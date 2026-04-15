const fs = require('fs');
const path = require('path');

const rootDir = process.cwd();

let errors = 0;
let warnings = 0;

function check(label, condition, isWarning = false) {
    if (condition) {
        console.log(`  ✅ ${label}`);
    } else if (isWarning) {
        console.log(`  ⚠️  ${label}`);
        warnings++;
    } else {
        console.log(`  ❌ ${label}`);
        errors++;
    }
}

function readJson(filePath) {
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch {
        return null;
    }
}

console.log('\n🔍 Obsidian Plugin Validation\n');

// 1. manifest.json
console.log('📄 manifest.json');
const manifestPath = path.join(rootDir, 'manifest.json');
const manifest = readJson(manifestPath);
check('File exists', manifest !== null);
if (manifest) {
    check('Has "id" field', !!manifest.id);
    check('Has "version" field', !!manifest.version);
    check('Has "name" field', !!manifest.name);
    check('Has "minAppVersion" field', !!manifest.minAppVersion);
}

// 2. package.json
console.log('\n📄 package.json');
const packagePath = path.join(rootDir, 'package.json');
const pkg = readJson(packagePath);
check('File exists', pkg !== null);
if (pkg && manifest) {
    check(
        `Version matches manifest (${pkg.version} === ${manifest.version})`,
        pkg.version === manifest.version
    );
}

// 3. main.js
console.log('\n📄 main.js');
const mainPath = path.join(rootDir, 'main.js');
const mainExists = fs.existsSync(mainPath);
check('File exists', mainExists);
if (mainExists) {
    const mainSize = fs.statSync(mainPath).size;
    check(`File is not empty (${(mainSize / 1024).toFixed(1)} KB)`, mainSize > 0);
}

// 4. styles.css
console.log('\n📄 styles.css');
const stylesPath = path.join(rootDir, 'styles.css');
check('File exists (optional)', fs.existsSync(stylesPath), true);

// 5. Git & GitHub
console.log('\n🔗 Git & GitHub');
const gitDir = path.join(rootDir, '.git');
check('.git directory exists', fs.existsSync(gitDir));

// Check for GitHub remote
try {
    const gitConfig = fs.readFileSync(path.join(gitDir, 'config'), 'utf8');
    const hasGitHub = gitConfig.includes('github.com');
    check('Remote points to GitHub', hasGitHub);
} catch {
    check('Remote points to GitHub', false);
}

// 6. .gitignore check
console.log('\n📄 .gitignore');
const gitignorePath = path.join(rootDir, '.gitignore');
if (fs.existsSync(gitignorePath)) {
    const gitignore = fs.readFileSync(gitignorePath, 'utf8');
    const blocksMain = gitignore.split('\n').some(
        line => line.trim() === 'main.js' || line.trim() === '*.js'
    );
    if (blocksMain) {
        console.log('  ⚠️  .gitignore may block main.js — use "git add -f main.js" when committing');
        warnings++;
    } else {
        console.log('  ✅ .gitignore does not block main.js');
    }
} else {
    console.log('  ✅ No .gitignore file (no blocking risk)');
}

// 7. versions.json
console.log('\n📄 versions.json');
const versionsPath = path.join(rootDir, 'versions.json');
check('File exists', fs.existsSync(versionsPath), true);

// 8. GitHub Actions
console.log('\n⚙️  GitHub Actions');
const workflowDir = path.join(rootDir, '.github', 'workflows');
const hasWorkflows = fs.existsSync(workflowDir);
check('.github/workflows exists', hasWorkflows, true);
if (hasWorkflows) {
    const files = fs.readdirSync(workflowDir);
    const hasRelease = files.some(f => f.includes('release'));
    check('Release workflow exists', hasRelease, true);
}

// Summary
console.log('\n' + '─'.repeat(40));
if (errors === 0 && warnings === 0) {
    console.log('🎉 All checks passed! Ready for release.\n');
} else if (errors === 0) {
    console.log(`⚠️  ${warnings} warning(s), 0 errors. Review warnings before release.\n`);
} else {
    console.log(`❌ ${errors} error(s), ${warnings} warning(s). Fix errors before release.\n`);
    process.exit(1);
}
