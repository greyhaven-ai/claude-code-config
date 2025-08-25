# Publishing Instructions

This document contains instructions for publishing Claude Config to npm and Homebrew.

## NPM Publishing

### Prerequisites
1. Create an npm account at https://www.npmjs.com/signup
2. Verify your email address
3. Enable 2FA (required for publishing)

### First-Time Setup
```bash
# Login to npm
npm login
# Enter your username, password, and email
# Enter your 2FA code when prompted
```

### Publishing Process

1. **Update version** (follow semantic versioning):
```bash
# For patch release (bug fixes): 1.0.0 -> 1.0.1
npm version patch

# For minor release (new features): 1.0.0 -> 1.1.0
npm version minor

# For major release (breaking changes): 1.0.0 -> 2.0.0
npm version major
```

2. **Test locally** before publishing:
```bash
# Pack the package
npm pack

# Install locally to test
npm install -g grey-haven-claude-config-1.0.0.tgz

# Test the CLI
claude-config --help
claude-config wizard

# Uninstall test version
npm uninstall -g @grey-haven/claude-config
```

3. **Publish to npm**:
```bash
# Dry run to see what will be published
npm publish --dry-run

# Publish to npm registry
npm publish

# If scoped package (@grey-haven/claude-config), ensure public access:
npm publish --access public
```

4. **Verify publication**:
```bash
# Check npm page
open https://www.npmjs.com/package/@grey-haven/claude-config

# Test installation
npm install -g @grey-haven/claude-config
```

### Updating Published Package

```bash
# Make your changes
# Update version
npm version patch  # or minor/major

# Publish update
npm publish

# Users can update with:
# npm update -g @grey-haven/claude-config
# or
# claude-config self-update
```

## Homebrew Publishing

### Prerequisites
1. GitHub account with admin access to grey-haven organization
2. Create a new repository: `grey-haven/homebrew-tools`

### Setting Up Homebrew Tap

1. **Create tap repository**:
```bash
# Create new repo on GitHub: grey-haven/homebrew-tools
# Clone it locally
git clone https://github.com/grey-haven/homebrew-tools.git
cd homebrew-tools
```

2. **Create Formula directory**:
```bash
mkdir -p Formula
```

3. **Copy formula file**:
```bash
cp ../grey-haven-claude-config/homebrew/claude-config.rb Formula/
```

4. **Create a GitHub release** in the main repo:
```bash
# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Create release on GitHub
# Go to: https://github.com/grey-haven/grey-haven-claude-config/releases
# Click "Create a new release"
# Choose the tag, add release notes
```

5. **Update formula with correct SHA256**:
```bash
# Download the release tarball
curl -L https://github.com/grey-haven/grey-haven-claude-config/archive/v1.0.0.tar.gz -o claude-config.tar.gz

# Get SHA256
shasum -a 256 claude-config.tar.gz
# Copy the hash

# Update Formula/claude-config.rb with the correct SHA256
```

6. **Commit and push formula**:
```bash
git add Formula/claude-config.rb
git commit -m "Add claude-config formula v1.0.0"
git push origin main
```

### User Installation

Once published, users can install with:
```bash
# Add the tap
brew tap grey-haven/tools

# Install claude-config
brew install claude-config

# Update
brew upgrade claude-config
```

## Release Checklist

Before each release:

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG is updated
- [ ] Version number is bumped
- [ ] Local testing completed
- [ ] Git tag created
- [ ] GitHub release created
- [ ] NPM package published
- [ ] Homebrew formula updated
- [ ] Announcement prepared

## Version Management

Current version: 1.0.0

Version scheme:
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

Examples:
- Adding new command: minor bump (1.0.0 -> 1.1.0)
- Fixing typo: patch bump (1.0.0 -> 1.0.1)
- Changing command syntax: major bump (1.0.0 -> 2.0.0)

## Troubleshooting

### NPM Issues

**403 Forbidden**:
- Ensure you're logged in: `npm whoami`
- Check package name isn't taken
- For scoped packages, use `--access public`

**E402 Payment Required**:
- Private packages require paid account
- Use `--access public` for free packages

**Version conflict**:
- Can't republish same version
- Bump version with `npm version patch`

### Homebrew Issues

**SHA256 mismatch**:
- Download the exact tarball from GitHub releases
- Recalculate SHA256
- Update formula

**Formula syntax errors**:
- Test locally: `brew install --build-from-source ./Formula/claude-config.rb`
- Check Ruby syntax

## Support Channels

- NPM Support: https://www.npmjs.com/support
- Homebrew Documentation: https://docs.brew.sh/
- GitHub Issues: https://github.com/grey-haven/grey-haven-claude-config/issues