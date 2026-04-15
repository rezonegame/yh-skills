const fs = require('fs');
const path = require('path');

const newVersion = process.argv[2];

if (!newVersion) {
    console.error('Usage: node bump_version.js <new_version>');
    console.error('Example: node bump_version.js 1.2.0');
    process.exit(1);
}

// Validate semver format (loose)
if (!/^\d+\.\d+\.\d+/.test(newVersion)) {
    console.error(`Error: "${newVersion}" is not a valid version format. Use x.y.z`);
    process.exit(1);
}

const rootDir = process.cwd();

function readJson(filePath) {
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    } catch {
        return null;
    }
}

function updateJson(filePath, updateFn) {
    const data = readJson(filePath);
    if (!data) {
        console.log(`  ⏭️  Skipped ${path.basename(filePath)} (not found)`);
        return null;
    }
    const updated = updateFn(data);
    fs.writeFileSync(filePath, JSON.stringify(updated, null, '\t') + '\n');
    console.log(`  ✅ Updated ${path.basename(filePath)}`);
    return updated;
}

// Detect old version
const currentPkg = readJson(path.join(rootDir, 'package.json'));
const oldVersion = currentPkg ? currentPkg.version : null;

console.log('\n📦 Obsidian Plugin Version Bump\n');
console.log(`  Old version: ${oldVersion || '(unknown)'}`);
console.log(`  New version: ${newVersion}\n`);

// 1. package.json
updateJson(path.join(rootDir, 'package.json'), (data) => {
    data.version = newVersion;
    return data;
});

// 2. manifest.json
let minAppVersion = '0.15.0';
updateJson(path.join(rootDir, 'manifest.json'), (data) => {
    data.version = newVersion;
    if (data.minAppVersion) minAppVersion = data.minAppVersion;
    return data;
});

// 3. manifest-beta.json (if exists)
updateJson(path.join(rootDir, 'manifest-beta.json'), (data) => {
    data.version = newVersion;
    return data;
});

// 4. versions.json
updateJson(path.join(rootDir, 'versions.json'), (data) => {
    data[newVersion] = minAppVersion;
    return data;
});

// 5. README.md (replace old version strings)
const readmePath = path.join(rootDir, 'README.md');
if (oldVersion && fs.existsSync(readmePath)) {
    let content = fs.readFileSync(readmePath, 'utf8');
    if (content.includes(oldVersion)) {
        content = content.split(oldVersion).join(newVersion);
        fs.writeFileSync(readmePath, content, 'utf8');
        console.log(`  ✅ Updated README.md (${oldVersion} → ${newVersion})`);
    } else {
        console.log(`  ⏭️  README.md does not contain "${oldVersion}"`);
    }
} else {
    console.log(`  ⏭️  Skipped README.md update`);
}

console.log(`\n🎉 Successfully bumped to ${newVersion}\n`);
