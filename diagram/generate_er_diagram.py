"""
Generate ER Diagram for Django Blog Project
Requires: erdantic, graphviz
Install: pip install erdantic
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'blogs'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import erdantic as erd
from blog.models import Post, Comment
from users.models import Profile

# Create ER diagram
diagram = erd.create(Post, Profile, Comment)

# Save as PNG and SVG
output_dir = os.path.join(os.path.dirname(__file__), 'er_diagram')
os.makedirs(output_dir, exist_ok=True)

diagram.draw(os.path.join(output_dir, 'er_diagram.png'))
diagram.draw(os.path.join(output_dir, 'er_diagram.svg'))

print("✓ ER Diagram generated successfully!")
print(f"  PNG: {os.path.join(output_dir, 'er_diagram.png')}")
print(f"  SVG: {os.path.join(output_dir, 'er_diagram.svg')}")
