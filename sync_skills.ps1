
$skills = @(
    'boardgame-boards', 'boardgame-boxes', 'boardgame-cards', 'boardgame-components', 
    'boardgame-design', 'boardgame-ralph-loop', 'boardgame-tiles', 'boardgame-writer',
    'content-research-writer', 'content-strategist', 'doc-coauthoring', 'ducksearch', 
    'humanizer-zh', 'last30days', 'literature-review', 'meeplelm', 
    'multi-agent-debate', 'openalex-database', 'scientific-critical-thinking', 'scientific-writing',
    'gamified-course-designer', 'geo-content-optimizer', 'khazix-writer', 'yh-slides', 
    'obsidian-plugin-release', 'merge-drafts', 'qiaomu-mondo-poster-design', 
    'anything-to-notebooklm', 'knowledge-site-creator', 'identity-design', 
    'unity-game-ui-toolkit-design', 'skill-manager'
)
$source = "C:\Users\wudao\.gemini\skills"
$dest = "d:\Github\yh-skills"

foreach ($skill in $skills) {
    if (Test-Path "$source\$skill") {
        Write-Host "Syncing $skill..."
        # Create destination directory if it doesn't exist
        if (!(Test-Path "$dest\$skill")) {
             New-Item -ItemType Directory -Force -Path "$dest\$skill" | Out-Null
        }
        # Sync the contents
        robocopy "$source\$skill" "$dest\$skill" /MIR /XD node_modules .git /NJH /NJS /NDL /NC /NS /R:3 /W:5
    } else {
        Write-Warning "Skill $skill not found in source."
    }
}
