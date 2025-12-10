"""
Generate ER Diagram as SVG/HTML for Django Blog Project
This script creates a visual ER diagram without requiring graphviz.
"""
import os

def generate_html_er_diagram():
    """Generate an interactive HTML ER diagram"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Blog - ER Diagram</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 1200px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 40px;
            font-size: 2.5em;
        }
        .diagram {
            display: flex;
            justify-content: space-around;
            align-items: flex-start;
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }
        .entity {
            background: #f8f9fa;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 20px;
            flex: 1;
            min-width: 250px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .entity:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        .entity-name {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 15px;
            border-radius: 6px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            font-size: 1.1em;
        }
        .fields {
            list-style: none;
        }
        .field {
            padding: 8px 10px;
            margin: 5px 0;
            background: white;
            border-left: 3px solid #667eea;
            font-size: 0.95em;
            border-radius: 3px;
        }
        .field.pk {
            font-weight: bold;
            background: #e7f3ff;
        }
        .field.fk {
            background: #fff4e7;
        }
        .field.unique {
            background: #e7f5e7;
            font-style: italic;
        }
        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.75em;
            font-weight: bold;
            margin-left: 5px;
        }
        .badge-pk {
            background: #dc3545;
            color: white;
        }
        .badge-fk {
            background: #fd7e14;
            color: white;
        }
        .badge-unique {
            background: #28a745;
            color: white;
        }
        .relationships {
            background: #f0f4ff;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 25px;
            margin-top: 30px;
        }
        .relationships h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.4em;
        }
        .relationship {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #764ba2;
            border-radius: 4px;
        }
        .relationship-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .relationship-details {
            color: #666;
            font-size: 0.95em;
            line-height: 1.5;
        }
        .connection {
            color: #764ba2;
            font-weight: bold;
        }
        .legend {
            background: #fff9e6;
            border: 1px solid #ffc107;
            border-radius: 6px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .legend-item {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Django Blog Project - ER Diagram</h1>
        
        <div class="diagram">
            <!-- User Entity -->
            <div class="entity">
                <div class="entity-name">👤 User (Auth)</div>
                <ul class="fields">
                    <li class="field pk">id <span class="badge badge-pk">PK</span></li>
                    <li class="field">username (varchar 150)</li>
                    <li class="field unique">email <span class="badge badge-unique">UNIQUE</span></li>
                    <li class="field">password (hashed)</li>
                    <li class="field">first_name</li>
                    <li class="field">last_name</li>
                    <li class="field">is_staff (bool)</li>
                    <li class="field">is_active (bool)</li>
                    <li class="field">date_joined (datetime)</li>
                </ul>
            </div>

            <!-- Post Entity -->
            <div class="entity">
                <div class="entity-name">📝 Post</div>
                <ul class="fields">
                    <li class="field pk">id <span class="badge badge-pk">PK</span></li>
                    <li class="field">title (varchar 100)</li>
                    <li class="field">content (FroalaField)</li>
                    <li class="field">image (optional)</li>
                    <li class="field">date_posted (datetime)</li>
                    <li class="field fk">author_id <span class="badge badge-fk">FK</span></li>
                </ul>
            </div>

            <!-- Profile Entity -->
            <div class="entity">
                <div class="entity-name">🎨 Profile</div>
                <ul class="fields">
                    <li class="field pk">id <span class="badge badge-pk">PK</span></li>
                    <li class="field fk unique">user_id <span class="badge badge-fk">FK</span> <span class="badge badge-unique">UNIQUE</span></li>
                    <li class="field">image (profile_pics)</li>
                </ul>
            </div>
        </div>

        <div class="relationships">
            <h2>🔗 Relationships</h2>
            
            <div class="relationship">
                <div class="relationship-title">1. Post → User (Many-to-One)</div>
                <div class="relationship-details">
                    <div><span class="connection">Cardinality:</span> N:1 (Many Posts per User)</div>
                    <div><span class="connection">Foreign Key:</span> Post.author_id → User.id</div>
                    <div><span class="connection">Delete:</span> CASCADE (delete post if user deleted)</div>
                    <div><span class="connection">Query:</span> user.post_set.all() OR Post.objects.filter(author=user)</div>
                </div>
            </div>

            <div class="relationship">
                <div class="relationship-title">2. Profile ↔ User (One-to-One)</div>
                <div class="relationship-details">
                    <div><span class="connection">Cardinality:</span> 1:1 (One Profile per User)</div>
                    <div><span class="connection">Foreign Key:</span> Profile.user_id → User.id (UNIQUE)</div>
                    <div><span class="connection">Delete:</span> CASCADE (delete profile if user deleted)</div>
                    <div><span class="connection">Query:</span> user.profile (reverse accessor)</div>
                </div>
            </div>

            <div class="legend">
                <strong>Legend:</strong>
                <div class="legend-item">🔴 <span class="badge badge-pk">PK</span> = Primary Key (unique identifier)</div>
                <div class="legend-item">🟠 <span class="badge badge-fk">FK</span> = Foreign Key (reference to another table)</div>
                <div class="legend-item">🟢 <span class="badge badge-unique">UNIQUE</span> = Unique constraint</div>
            </div>
        </div>

        <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
            <h3 style="color: #667eea; margin-bottom: 15px;">📊 Database Tables Generated</h3>
            <ul style="line-height: 2; color: #555;">
                <li><strong>auth_user</strong> - Django built-in User model</li>
                <li><strong>blog_post</strong> - Blog posts from blog app</li>
                <li><strong>users_profile</strong> - User profiles from users app</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    output_path = os.path.join(os.path.dirname(__file__), 'er_diagram.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path


if __name__ == '__main__':
    output_path = generate_html_er_diagram()
    print(f"✓ ER Diagram generated successfully!")
    print(f"  📄 HTML: {output_path}")
    print(f"\n  Open this file in your browser to view the interactive ER diagram.")
