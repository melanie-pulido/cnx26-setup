#!/bin/bash
# CNX26 Setup Script for AI Expert Suite
# Automates repo cloning and dependency installation

set -e  # Exit on error

echo "🚀 CNX26 Marketing Cloud Setup"
echo "================================"
echo ""

# Check if already in the repo
if [ -f "CLAUDE.md" ] && [ -d ".claude" ]; then
    echo "✅ Already in cnx26-setup directory"
    SETUP_DIR=$(pwd)
else
    # Clone the repository
    echo "📦 Cloning repository..."
    if [ -d "cnx26-setup" ]; then
        echo "⚠️  Directory 'cnx26-setup' already exists. Using existing directory."
        cd cnx26-setup
        git pull origin main
    else
        git clone https://github.com/melanie-pulido/cnx26-setup.git
        cd cnx26-setup
    fi
    SETUP_DIR=$(pwd)
    echo "✅ Repository ready at: $SETUP_DIR"
fi

echo ""

# Check Python
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.x"
    exit 1
fi

echo ""

# Install dependencies
echo "📚 Installing Python dependencies..."
if pip3 install requests > /dev/null 2>&1; then
    echo "✅ Dependencies installed"
else
    echo "⚠️  Could not install dependencies automatically"
    echo "   Run: pip3 install requests"
fi

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📂 Project location: $SETUP_DIR"
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Open AI Expert Suite"
echo "2. Click the workspace selector (top-left corner)"
echo "3. Choose 'Open folder...'"
echo "4. Navigate to: $SETUP_DIR"
echo "5. Select the folder and click 'Open'"
echo ""
echo "Once opened, you can use these slash commands:"
echo "  • /create-cnx26-bu         - Create Business Unit"
echo "  • /create-cnx26-students   - Create student accounts"
echo "  • /deploy-mc-package       - Deploy MC package"
echo ""
echo "📖 For manual usage, see: $SETUP_DIR/README.md"
echo ""
