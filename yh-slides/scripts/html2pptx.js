/**
 * html2pptx.js — HTML 幻灯片 → PPTX 转换器
 *
 * 输入规范:
 *   - Body 尺寸: width: 720pt; height: 405pt (16:9)
 *   - 文字标签: <h1>-<h6>, <p>, <ul>, <ol>, <li>
 *   - 装饰标签: <div> (仅背景/边框)
 *   - 图片标签: <img>
 *   - 无 CSS 渐变，仅 web-safe 字体
 *   - 定位方式: inline style (left, top, width, height)
 *
 * 用法 (模块):
 *   const html2pptx = require('./html2pptx');
 *   await html2pptx('slide.html', pptx);
 *
 * 用法 (CLI):
 *   node html2pptx.js slide1.html slide2.html -o output.pptx
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

// ── 常量 ──────────────────────────────────────────────────────
const PT_PER_INCH = 72;
const SLIDE_WIDTH_PT = 720;
const SLIDE_HEIGHT_PT = 405;

// ── 工具函数 ──────────────────────────────────────────────────

/** pt 值转 inches */
function ptToIn(pt) {
  return pt / PT_PER_INCH;
}

/** 解析 CSS 值为 pt 数值 (支持 pt, px, in, em) */
function parseLength(val) {
  if (!val || val === 'auto' || val === 'inherit') return null;
  const m = val.match(/^([-\d.]+)(pt|px|in|em|%)?$/);
  if (!m) return null;
  const num = parseFloat(m[1]);
  const unit = m[2] || 'pt';
  switch (unit) {
    case 'pt': return num;
    case 'px': return num * 0.75;     // 96dpi → 72dpi
    case 'in': return num * 72;
    case 'em': return num * 16;       // 近似
    case '%':  return null;           // 百分比需要上下文，暂不支持
    default:   return num;
  }
}

/** 解析颜色字符串为 hex (不带 #) */
function parseColor(str) {
  if (!str) return null;
  str = str.trim();
  // hex: #RGB, #RRGGBB
  if (/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(str)) {
    return str.slice(1).toUpperCase();
  }
  // rgb(r, g, b)
  const rgb = str.match(/rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/);
  if (rgb) {
    const r = parseInt(rgb[1]).toString(16).padStart(2, '0');
    const g = parseInt(rgb[2]).toString(16).padStart(2, '0');
    const b = parseInt(rgb[3]).toString(16).padStart(2, '0');
    return (r + g + b).toUpperCase();
  }
  // rgba — 忽略 alpha，pptxgenjs 用 transparency 属性
  const rgba = str.match(/rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([-\d.]+)\s*\)/);
  if (rgba) {
    const r = parseInt(rgba[1]).toString(16).padStart(2, '0');
    const g = parseInt(rgba[2]).toString(16).padStart(2, '0');
    const b = parseInt(rgba[3]).toString(16).padStart(2, '0');
    return (r + g + b).toUpperCase();
  }
  return null;
}

/** 从 inline style 字符串解析为键值对象 */
function parseStyle(styleStr) {
  const result = {};
  if (!styleStr) return result;
  styleStr.split(';').forEach(decl => {
    const [k, ...rest] = decl.split(':');
    if (k && rest.length) {
      result[k.trim()] = rest.join(':').trim();
    }
  });
  return result;
}

/** 从 style 中提取位置和尺寸 (返回 inches) */
function parsePosition(style) {
  const pos = {};
  const left = parseLength(style.left || style['margin-left']);
  const top = parseLength(style.top || style['margin-top']);
  const width = parseLength(style.width);
  const height = parseLength(style.height);
  if (left !== null)   pos.x = ptToIn(left);
  if (top !== null)    pos.y = ptToIn(top);
  if (width !== null)  pos.w = ptToIn(width);
  if (height !== null) pos.h = ptToIn(height);
  return pos;
}

/** 解析 border shorthand: "1px solid #000000" */
function parseBorder(borderStr) {
  if (!borderStr || borderStr === 'none') return null;
  const m = borderStr.match(/^([-\d.]+)(px|pt)\s+(solid|dashed|dotted)\s+(.+)$/);
  if (!m) return null;
  const widthVal = parseFloat(m[1]);
  const unit = m[2];
  const style = m[3];
  const colorStr = m[4];
  return {
    width: unit === 'pt' ? widthVal : widthVal * 0.75,
    dashType: style === 'dashed' ? 'dash' : style === 'dotted' ? 'dot' : undefined,
    color: parseColor(colorStr)
  };
}

/** 标题标签 → 字号映射 (pt) */
function headingSize(tag) {
  const map = { h1: 36, h2: 30, h3: 26, h4: 22, h5: 20, h6: 18 };
  return map[tag] || 18;
}

// ── 核心转换 ──────────────────────────────────────────────────

/**
 * 将单个 HTML 文件转换为一个 PPTX 幻灯片并添加到 pptx 对象
 * @param {string} htmlPath - HTML 文件路径
 * @param {object} pptx - pptxgenjs 实例
 * @param {object} [opts] - 可选配置
 */
async function html2pptx(htmlPath, pptx, opts = {}) {
  const htmlDir = path.dirname(path.resolve(htmlPath));
  const html = fs.readFileSync(htmlPath, 'utf-8');
  const $ = cheerio.load(html);

  const slide = pptx.addSlide();

  // ── 1. 页面背景 ──
  const bodyStyle = parseStyle($('body').attr('style') || '');
  const bodyBg = parseColor(bodyStyle['background-color'] || bodyStyle.background);
  if (bodyBg) {
    slide.background = { color: bodyBg };
  }

  // ── 2. 遍历 body 子元素 ──
  const children = $('body').children().toArray();

  for (const el of children) {
    const $el = $(el);
    const tag = el.tagName.toLowerCase();
    const style = parseStyle($el.attr('style') || '');

    switch (tag) {
      // ── 装饰形状 ──
      case 'div': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        const bgColor = parseColor(style['background-color'] || style.background);
        const border = parseBorder(style.border) ||
                       parseBorder(style['border-top']) ||
                       parseBorder(style['border-bottom']);

        const shapeOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(100),
          h: pos.h || ptToIn(50)
        };
        if (bgColor) shapeOpts.fill = { color: bgColor };

        // 透明度
        if (style.opacity) {
          shapeOpts.transparency = Math.round((1 - parseFloat(style.opacity)) * 100);
        }

        // 边框
        if (border && border.color) {
          shapeOpts.line = {
            color: border.color,
            width: border.width
          };
          if (border.dashType) shapeOpts.line.dashType = border.dashType;
        }

        // 圆角 (近似: 使用 ROUNDED_RECTANGLE)
        if (style['border-radius']) {
          const r = parseLength(style['border-radius']);
          if (r !== null && r > 0) {
            slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
              ...shapeOpts,
              rectRadius: ptToIn(r)
            });
            break;
          }
        }

        slide.addShape(pptx.shapes.RECTANGLE, shapeOpts);
        break;
      }

      // ── 标题文字 ──
      case 'h1': case 'h2': case 'h3':
      case 'h4': case 'h5': case 'h6': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        const textContent = $el.text().trim();
        if (!textContent) break;

        const color = parseColor(style.color);
        const fontSize = parseLength(style['font-size']) || headingSize(tag);

        const textOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(640),
          h: pos.h || ptToIn(fontSize * 2),
          fontSize: fontSize,
          fontFace: style['font-family']?.replace(/['"]/g, '').split(',')[0]?.trim() || 'Arial',
          bold: true,
          color: color || '1A3C5E',
          margin: 0
        };

        if (style['text-align']) textOpts.align = style['text-align'];

        slide.addText(textContent, textOpts);
        break;
      }

      // ── 段落文字 ──
      case 'p': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        const textContent = $el.html();
        if (!textContent) break;

        const textRuns = parseRichText($, $el, style);
        const color = parseColor(style.color);
        const fontSize = parseLength(style['font-size']) || 16;

        const textOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(640),
          h: pos.h || ptToIn(200),
          fontSize: fontSize,
          fontFace: style['font-family']?.replace(/['"]/g, '').split(',')[0]?.trim() || 'Arial',
          color: color || '2D3436',
          valign: 'top',
          margin: 0
        };

        if (style['text-align']) textOpts.align = style['text-align'];
        if (style['line-height']) {
          const lh = parseFloat(style['line-height']);
          if (!isNaN(lh)) textOpts.lineSpacingMultiple = lh;
        }

        slide.addText(textRuns, textOpts);
        break;
      }

      // ── 无序列表 ──
      case 'ul': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        const items = [];
        $el.children('li').each((_, li) => {
          const $li = $(li);
          const liStyle = parseStyle($li.attr('style') || '');
          items.push({
            text: $li.text().trim(),
            options: {
              bullet: true,
              breakLine: true,
              fontSize: parseLength(liStyle['font-size']) || parseLength(style['font-size']) || 16,
              color: parseColor(liStyle.color || style.color) || '2D3436'
            }
          });
        });

        if (items.length > 0) {
          // 移除最后一项的 breakLine
          items[items.length - 1].options.breakLine = false;
        }

        const textOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(640),
          h: pos.h || ptToIn(250),
          fontFace: style['font-family']?.replace(/['"]/g, '').split(',')[0]?.trim() || 'Arial',
          valign: 'top',
          paraSpaceAfter: 6,
          margin: 0
        };

        if (style['text-align']) textOpts.align = style['text-align'];

        slide.addText(items, textOpts);
        break;
      }

      // ── 有序列表 ──
      case 'ol': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        const items = [];
        $el.children('li').each((_, li) => {
          const $li = $(li);
          const liStyle = parseStyle($li.attr('style') || '');
          items.push({
            text: $li.text().trim(),
            options: {
              bullet: { type: 'number' },
              breakLine: true,
              fontSize: parseLength(liStyle['font-size']) || parseLength(style['font-size']) || 16,
              color: parseColor(liStyle.color || style.color) || '2D3436'
            }
          });
        });

        if (items.length > 0) {
          items[items.length - 1].options.breakLine = false;
        }

        const textOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(640),
          h: pos.h || ptToIn(250),
          fontFace: style['font-family']?.replace(/['"]/g, '').split(',')[0]?.trim() || 'Arial',
          valign: 'top',
          paraSpaceAfter: 6,
          margin: 0
        };

        if (style['text-align']) textOpts.align = style['text-align'];

        slide.addText(items, textOpts);
        break;
      }

      // ── 图片 ──
      case 'img': {
        const pos = parsePosition(style);
        if (pos.x == null || pos.y == null) break;

        let src = $el.attr('src') || $el.attr('data-src');
        if (!src) break;

        const imgOpts = {
          x: pos.x,
          y: pos.y,
          w: pos.w || ptToIn(200),
          h: pos.h || ptToIn(200)
        };

        // base64 data URI
        if (src.startsWith('data:')) {
          imgOpts.data = src;
        } else {
          // 相对路径 → 基于 HTML 文件目录解析
          const absPath = path.resolve(htmlDir, src);
          imgOpts.path = absPath;
        }

        if (style['object-fit'] === 'contain') {
          imgOpts.sizing = { type: 'contain', w: imgOpts.w, h: imgOpts.h };
        } else if (style['object-fit'] === 'cover') {
          imgOpts.sizing = { type: 'cover', w: imgOpts.w, h: imgOpts.h };
        }

        slide.addImage(imgOpts);
        break;
      }

      default:
        // 忽略未知标签
        break;
    }
  }

  return slide;
}

/**
 * 解析富文本 (含 <strong>, <em>, <span> 等) 为 pptxgenjs textRuns 数组
 */
function parseRichText($, $el, parentStyle) {
  const runs = [];
  const nodes = $el.contents().toArray();

  for (const node of nodes) {
    if (node.type === 'text') {
      const text = node.data;
      if (text.trim()) {
        runs.push({
          text: text,
          options: {
            fontSize: parseLength(parentStyle['font-size']) || 16,
            color: parseColor(parentStyle.color) || '2D3436'
          }
        });
      }
    } else if (node.type === 'tag') {
      const $node = $(node);
      const tag = node.tagName.toLowerCase();
      const style = parseStyle($node.attr('style') || '');

      const runOpts = {
        fontSize: parseLength(style['font-size']) || parseLength(parentStyle['font-size']) || 16,
        color: parseColor(style.color || parentStyle.color) || '2D3436'
      };

      if (tag === 'strong' || tag === 'b') runOpts.bold = true;
      if (tag === 'em' || tag === 'i') runOpts.italic = true;
      if (style['text-decoration']?.includes('underline')) runOpts.underline = { style: 'sng' };

      runs.push({
        text: $node.text(),
        options: runOpts
      });
    }
  }

  // 如果没有解析到富文本元素，返回纯文本单条
  if (runs.length === 0) {
    runs.push({
      text: $el.text().trim(),
      options: {
        fontSize: parseLength(parentStyle['font-size']) || 16,
        color: parseColor(parentStyle.color) || '2D3436'
      }
    });
  }

  return runs;
}

// ── CLI 入口 ──────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const htmlFiles = [];
  let outputFile = 'output.pptx';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-o' || args[i] === '--output') {
      outputFile = args[++i];
    } else if (!args[i].startsWith('-')) {
      htmlFiles.push(args[i]);
    }
  }

  if (htmlFiles.length === 0) {
    console.error('用法: node html2pptx.js <slide1.html> [slide2.html ...] -o output.pptx');
    process.exit(1);
  }

  const pptxgen = require('pptxgenjs');
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';

  for (const f of htmlFiles) {
    console.log(`转换: ${f}`);
    await html2pptx(f, pptx);
  }

  await pptx.writeFile({ fileName: outputFile });
  console.log(`输出: ${outputFile}`);
}

// 如果直接运行（非被 require），执行 CLI
if (require.main === module) {
  main().catch(err => {
    console.error('错误:', err.message);
    process.exit(1);
  });
}

module.exports = html2pptx;
