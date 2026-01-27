import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os


COLORS = {
    'Feature': '#AED6F1',      # Blue
    'Dependency': '#E74C3C',   # Red
    'Milestone': '#F39C12',    # Orange
    'Line': '#C0392B',         # String
    'IP_Fill': '#FADBD8'       # Light Red
}

ITERATIONS = ['Iteration 1.1', 'Iteration 1.2', 'Iteration 1.3', 'Iteration 1.4', 'Iteration 1.5 (IP)', 'PI 2 >>>']
TEAMS = ['Milestones & Events', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta']

def generate_fixed_art_board(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    df['Iteration'] = df['Iteration'].str.replace('Iteration 1.5', 'Iteration 1.5 (IP)')
    
    fig, ax = plt.subplots(figsize=(22, 12))
    ax.set_xlim(-0.5, len(ITERATIONS) - 0.5)
    ax.set_ylim(-0.5, len(TEAMS) - 0.5)
    
    # Background Grid
    for i in range(len(ITERATIONS) + 1): ax.axvline(i - 0.5, color='#BDC3C7', lw=0.8, ls='--')
    for j in range(len(TEAMS) + 1): ax.axhline(j - 0.5, color='#BDC3C7', lw=0.8)

    # IP Iteration Blackout
    ip_idx = ITERATIONS.index('Iteration 1.5 (IP)')
    ax.add_patch(patches.Rectangle((ip_idx - 0.5, -0.5), 1, len(TEAMS), color=COLORS['IP_Fill'], alpha=0.25))
    ax.text(ip_idx, 0.4, "IP ITERATION: NO FEATURE WORK", ha='center', fontweight='bold', color='#A93226', fontsize=10)

    pos_map = {}
    id_to_type = {}
    cell_occupancy = {} 

    # Card Rendering
    for _, row in df.iterrows():
        it_key = row['Iteration']
        x = ITERATIONS.index(it_key)
        y = TEAMS.index('Milestones & Events') if row['Type'] in ['Milestone', 'Event'] else TEAMS.index(row['Team'])
        
        count = cell_occupancy.get((x, y), 0)
        y_offset = count * 0.18  
        cell_occupancy[(x, y)] = count + 1

        is_source = df['Dependency_ID'].str.contains(row['ID'], na=False).any()
        if row['Type'] in ['Milestone', 'Event']:
            color, c_type = COLORS['Milestone'], 'ORANGE'
        elif is_source:
            color, c_type = COLORS['Dependency'], 'RED'
        else:
            color, c_type = COLORS['Feature'], 'BLUE'

        rect = patches.FancyBboxPatch((x - 0.38, y - 0.28 + y_offset), 0.76, 0.50, 
                                      boxstyle="round,pad=0.02", lw=1.5, 
                                      edgecolor='#283747', facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y + y_offset, f"{row['ID']}\n{row['Subject']}", 
                ha='center', va='center', fontsize=8, fontweight='bold', wrap=True)
        
        pos_map[row['ID']] = (x, y + y_offset)
        id_to_type[row['ID']] = c_type

 
    for _, row in df.iterrows():
        if pd.notna(row['Dependency_ID']):
            src, tgt = row['Dependency_ID'], row['ID']
            if src in pos_map and tgt in pos_map:
                if id_to_type[src] != 'ORANGE': 
                    ax.annotate("", xy=pos_map[tgt], xytext=pos_map[src],
                                arrowprops=dict(arrowstyle="->", color=COLORS['Line'],
                                                connectionstyle="arc3,rad=.2", lw=2, alpha=0.5))


    ax.set_xticks(range(len(ITERATIONS)))
    ax.set_xticklabels(ITERATIONS, fontsize=12, fontweight='bold')
    ax.set_yticks(range(len(TEAMS)))
    ax.set_yticklabels(TEAMS, fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    
    plt.title("ENTERPRISE ART PLANNING: MULTI-TEAM DEPENDENCY ORCHESTRATION", 
              fontsize=22, fontweight='bold', pad=40)
    
    os.makedirs("output_visuals", exist_ok=True)
    save_path = "output_visuals/art_board_fixed_stacking.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Fixed board generated: {save_path}")

if __name__ == "__main__":
    generate_fixed_art_board('art_program_board_final_v4.csv')
