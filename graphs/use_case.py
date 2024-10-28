from graphviz import Digraph


def create_budget_tool_usecase():
    dot = Digraph(comment='AI Budget Tool Use Case Diagram')
    dot.attr(rankdir='LR')
    dot.attr(fontname='Arial')

    # Define system boundary
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='AI Personal Budget Tool System')
        c.attr(style='rounded')

        # Core Budget Management Use Cases
        c.node('UC1', 'Create/Modify Budget\nLimits', shape='ellipse')
        c.node('UC2', 'Track Expenses', shape='ellipse')
        c.node('UC3', 'Categorize\nTransactions', shape='ellipse')
        c.node('UC4', 'View Spending\nAnalytics', shape='ellipse')

        # AI-Driven Features
        c.node('UC5', 'Receive AI-Driven\nInsights', shape='ellipse')
        c.node('UC6', 'Get Personalized\nBudget Recommendations', shape='ellipse')
        c.node('UC7', 'View Spending\nPredictions', shape='ellipse')
        c.node('UC8', 'Get Real-time\nFinancial Advice', shape='ellipse')

        # Account Management
        c.node('UC9', 'Manage User Profile', shape='ellipse')
        c.node('UC10', 'Authentication', shape='ellipse')

        # Include relationships
        c.edge('UC2', 'UC3', 'includes', style='dashed')
        c.edge('UC2', 'UC4', 'includes', style='dashed')
        c.edge('UC4', 'UC5', 'includes', style='dashed')
        c.edge('UC5', 'UC6', 'includes', style='dashed')
        c.edge('UC5', 'UC7', 'includes', style='dashed')

    # Define actors - using custom shape settings for better actor representation
    dot.node('User', 'Regular User', shape='box', style='rounded')
    dot.node('Admin', 'Administrator', shape='box', style='rounded')
    dot.node('AI', 'ChatGPT API', shape='component')

    # User relationships
    dot.edge('User', 'UC1')
    dot.edge('User', 'UC2')
    dot.edge('User', 'UC4')
    dot.edge('User', 'UC5')
    dot.edge('User', 'UC8')
    dot.edge('User', 'UC9')
    dot.edge('User', 'UC10')

    # Admin relationships
    dot.edge('Admin', 'UC10')
    dot.edge('Admin', 'UC9')

    # AI relationships
    dot.edge('AI', 'UC5')
    dot.edge('AI', 'UC6')
    dot.edge('AI', 'UC7')
    dot.edge('AI', 'UC8')

    return dot


# Create and save the diagram
diagram = create_budget_tool_usecase()
diagram.render('./graphs/output/budget_tool_usecase', format='png', cleanup=True)
