"""
MIKE AI - Business & Side Hustle Agent
Generates side hustle ideas, creates business plans, tracks income, and provides growth strategies
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import random

class BusinessAgent:
    """Agent for generating and managing side hustles and business opportunities"""
    
    def __init__(self, config_path: str = None):
        self.name = "Business Agent"
        self.config_path = config_path or "config/business_config.json"
        self.business_ideas = []
        self.active_projects = []
        self.income_tracking = []
        self.load_config()
    
    def load_config(self):
        """Load business configuration"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.user_skills = config.get('user_skills', [])
                self.interests = config.get('interests', [])
                available_time = config.get('available_time_hours', 10)
                budget = config.get('startup_budget', 1000)
        else:
            self.user_skills = []
            self.interests = []
            available_time = 10
            budget = 1000
        
        self.available_time = available_time
        self.startup_budget = budget
    
    def save_config(self):
        """Save business configuration"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'user_skills': self.user_skills,
            'interests': self.interests,
            'available_time_hours': self.available_time,
            'startup_budget': self.startup_budget,
            'last_updated': datetime.now().isoformat()
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def setup_profile(self, skills: List[str], interests: List[str], 
                     available_hours: int = 10, budget: float = 1000):
        """Setup user business profile"""
        self.user_skills = skills
        self.interests = interests
        self.available_time = available_hours
        self.startup_budget = budget
        self.save_config()
        
        return {
            'success': True,
            'message': 'Business profile configured',
            'profile': {
                'skills': skills,
                'interests': interests,
                'time_available': f'{available_hours} hours/week',
                'budget': f'${budget}'
            }
        }
    
    def generate_ideas(self, count: int = 10, category: str = None) -> Dict:
        """
        Generate personalized side hustle ideas based on user profile
        Categories: online, offline, tech, creative, service, investment
        """
        print(f"[BUSINESS] Generating {count} side hustle ideas...")
        
        all_ideas = {
            'tech': [
                {'name': 'Freelance Web Development', 'startup_cost': 0, 'potential_monthly': '$500-$5000', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'Mobile App Development', 'startup_cost': 0, 'potential_monthly': '$1000-$10000', 'difficulty': 'Hard', 'time_required': '15-30 hrs/week'},
                {'name': 'AI Chatbot Services', 'startup_cost': 100, 'potential_monthly': '$800-$8000', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'WordPress Plugin Development', 'startup_cost': 0, 'potential_monthly': '$300-$3000', 'difficulty': 'Medium', 'time_required': '8-15 hrs/week'},
                {'name': 'Technical Consulting', 'startup_cost': 0, 'potential_monthly': '$1000-$15000', 'difficulty': 'Medium', 'time_required': '5-15 hrs/week'},
            ],
            'creative': [
                {'name': 'Digital Art & NFT Creation', 'startup_cost': 50, 'potential_monthly': '$200-$5000', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'Content Writing/Blogging', 'startup_cost': 0, 'potential_monthly': '$300-$4000', 'difficulty': 'Easy', 'time_required': '8-15 hrs/week'},
                {'name': 'YouTube Channel', 'startup_cost': 200, 'potential_monthly': '$100-$10000+', 'difficulty': 'Medium', 'time_required': '10-25 hrs/week'},
                {'name': 'Podcast Production', 'startup_cost': 300, 'potential_monthly': '$200-$5000', 'difficulty': 'Medium', 'time_required': '8-20 hrs/week'},
                {'name': 'Online Course Creation', 'startup_cost': 100, 'potential_monthly': '$500-$20000', 'difficulty': 'Medium', 'time_required': '20-40 hrs (initial)'},
            ],
            'service': [
                {'name': 'Virtual Assistant', 'startup_cost': 0, 'potential_monthly': '$400-$3000', 'difficulty': 'Easy', 'time_required': '10-25 hrs/week'},
                {'name': 'Social Media Management', 'startup_cost': 0, 'potential_monthly': '$500-$5000', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'Online Tutoring', 'startup_cost': 0, 'potential_monthly': '$300-$3000', 'difficulty': 'Easy', 'time_required': '5-15 hrs/week'},
                {'name': 'Bookkeeping Services', 'startup_cost': 100, 'potential_monthly': '$600-$6000', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'Translation Services', 'startup_cost': 0, 'potential_monthly': '$400-$4000', 'difficulty': 'Medium', 'time_required': '8-15 hrs/week'},
            ],
            'online': [
                {'name': 'Affiliate Marketing', 'startup_cost': 100, 'potential_monthly': '$100-$10000+', 'difficulty': 'Medium', 'time_required': '10-20 hrs/week'},
                {'name': 'Dropshipping Store', 'startup_cost': 500, 'potential_monthly': '$200-$15000', 'difficulty': 'Hard', 'time_required': '15-30 hrs/week'},
                {'name': 'Print on Demand', 'startup_cost': 100, 'potential_monthly': '$200-$5000', 'difficulty': 'Easy', 'time_required': '5-15 hrs/week'},
                {'name': 'Stock Photography', 'startup_cost': 200, 'potential_monthly': '$100-$2000', 'difficulty': 'Easy', 'time_required': '5-10 hrs/week'},
                {'name': 'Domain Flipping', 'startup_cost': 200, 'potential_monthly': '$100-$5000', 'difficulty': 'Medium', 'time_required': '5-10 hrs/week'},
            ],
            'investment': [
                {'name': 'Dividend Stock Investing', 'startup_cost': 1000, 'potential_monthly': '$10-$500 (passive)', 'difficulty': 'Easy', 'time_required': '2-5 hrs/week'},
                {'name': 'Crypto Staking', 'startup_cost': 500, 'potential_monthly': 'Variable', 'difficulty': 'Medium', 'time_required': '2-5 hrs/week'},
                {'name': 'Peer-to-Peer Lending', 'startup_cost': 1000, 'potential_monthly': '$20-$300', 'difficulty': 'Easy', 'time_required': '1-3 hrs/week'},
                {'name': 'REITs Investment', 'startup_cost': 500, 'potential_monthly': '$10-$200 (passive)', 'difficulty': 'Easy', 'time_required': '1-2 hrs/week'},
                {'name': 'Index Fund Investing', 'startup_cost': 500, 'potential_monthly': '$20-$500 (passive)', 'difficulty': 'Easy', 'time_required': '1-2 hrs/week'},
            ]
        }
        
        # Filter by category if specified
        if category and category.lower() in all_ideas:
            filtered_ideas = all_ideas[category.lower()]
        else:
            # Combine all categories
            filtered_ideas = []
            for cat_ideas in all_ideas.values():
                filtered_ideas.extend(cat_ideas)
        
        # Filter by budget
        affordable_ideas = [
            idea for idea in filtered_ideas 
            if idea['startup_cost'] <= self.startup_budget
        ]
        
        # If not enough affordable ideas, include some slightly over budget
        if len(affordable_ideas) < count:
            affordable_ideas = filtered_ideas[:count]
        
        # Sort by potential ROI
        affordable_ideas = sorted(affordable_ideas, key=lambda x: x['startup_cost'])[:count]
        
        # Add personalization score
        for idea in affordable_ideas:
            idea['personalization_score'] = self._calculate_fit_score(idea)
            idea['id'] = f'bizz_{random.randint(10000, 99999)}'
            idea['generated_at'] = datetime.now().isoformat()
        
        self.business_ideas = affordable_ideas
        
        return {
            'success': True,
            'total_generated': len(affordable_ideas),
            'filter_applied': {
                'category': category or 'all',
                'max_startup_cost': self.startup_budget,
                'available_time': f'{self.available_time} hrs/week'
            },
            'ideas': affordable_ideas,
            'top_recommendation': affordable_ideas[0] if affordable_ideas else None
        }
    
    def _calculate_fit_score(self, idea: Dict) -> int:
        """Calculate how well an idea fits user profile (0-100)"""
        score = 50  # Base score
        
        # Adjust based on difficulty vs experience (simplified)
        if idea['difficulty'] == 'Easy':
            score += 20
        elif idea['difficulty'] == 'Medium':
            score += 10
        
        # Adjust based on time fit
        idea_hours = int(idea['time_required'].split('-')[0])
        if idea_hours <= self.available_time:
            score += 20
        elif idea_hours <= self.available_time * 1.5:
            score += 10
        
        # Adjust based on budget fit
        if idea['startup_cost'] <= self.startup_budget * 0.5:
            score += 10
        
        return min(score, 100)
    
    def create_business_plan(self, idea_name: str) -> Dict:
        """Generate a detailed business plan for a selected idea"""
        print(f"[BUSINESS] Creating business plan for: {idea_name}")
        
        # Find the idea
        idea = next((i for i in self.business_ideas if i['name'] == idea_name), None)
        if not idea:
            # Create generic plan
            idea = {
                'name': idea_name,
                'startup_cost': 500,
                'potential_monthly': '$500-$5000',
                'difficulty': 'Medium'
            }
        
        plan = {
            'business_name': idea_name,
            'executive_summary': f"{idea_name} is a promising side hustle opportunity with potential monthly earnings of {idea['potential_monthly']}.",
            'market_analysis': {
                'target_audience': 'Identify your ideal customers',
                'market_size': 'Research market demand',
                'competition': 'Analyze competitors',
                'trends': 'Current industry trends favor this business'
            },
            'services_products': {
                'core_offering': f'Define your main {idea_name.lower()} service/product',
                'pricing_strategy': 'Competitive pricing with value-based options',
                'unique_value': 'What makes you different'
            },
            'marketing_plan': {
                'channels': ['Social Media', 'Content Marketing', 'Networking', 'Paid Ads'],
                'budget_allocation': {
                    'digital_marketing': '40%',
                    'content_creation': '30%',
                    'tools_software': '20%',
                    'miscellaneous': '10%'
                },
                'timeline': '3-month launch plan'
            },
            'financial_projections': {
                'startup_costs': {
                    'equipment': idea['startup_cost'] * 0.4,
                    'software_tools': idea['startup_cost'] * 0.2,
                    'marketing': idea['startup_cost'] * 0.3,
                    'contingency': idea['startup_cost'] * 0.1
                },
                'monthly_expenses': estimate_monthly_expenses(idea_name),
                'revenue_projections': {
                    'month_1': '$0-$500',
                    'month_3': '$500-$2000',
                    'month_6': '$2000-$5000',
                    'year_1': '$5000-$15000/month'
                },
                'break_even_timeline': '2-4 months'
            },
            'action_plan': {
                'week_1': ['Research market', 'Set up business structure', 'Create brand identity'],
                'week_2': ['Build online presence', 'Create portfolio/samples', 'Set pricing'],
                'week_3': ['Launch marketing campaigns', 'Network with potential clients', 'Gather testimonials'],
                'week_4': ['Analyze results', 'Optimize approach', 'Scale successful strategies'],
                'month_2_3': ['Expand service offerings', 'Increase marketing budget', 'Build team if needed']
            },
            'risk_analysis': {
                'risks': [
                    'Market saturation',
                    'Economic downturns',
                    'Technology changes',
                    'Time management challenges'
                ],
                'mitigation_strategies': [
                    'Differentiate through quality and service',
                    'Maintain emergency fund',
                    'Continuous learning',
                    'Automate where possible'
                ]
            },
            'success_metrics': [
                'Monthly revenue targets',
                'Customer acquisition rate',
                'Customer satisfaction score',
                'Time invested vs returns',
                'Profit margins'
            ]
        }
        
        self.active_projects.append({
            'name': idea_name,
            'plan': plan,
            'started_at': datetime.now().isoformat(),
            'status': 'planning'
        })
        
        return {
            'success': True,
            'business_plan': plan,
            'message': f'Comprehensive business plan created for {idea_name}'
        }
    
    def track_income(self, project_name: str, amount: float, 
                     date: str = None, category: str = 'revenue') -> Dict:
        """Track income and expenses for side hustles"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        entry = {
            'id': f'inc_{random.randint(10000, 99999)}',
            'project': project_name,
            'amount': amount,
            'date': date,
            'category': category,
            'recorded_at': datetime.now().isoformat()
        }
        
        self.income_tracking.append(entry)
        
        # Save to file
        income_file = Path("data/income_tracking.json")
        income_file.parent.mkdir(parents=True, exist_ok=True)
        
        existing_data = []
        if income_file.exists():
            with open(income_file, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.append(entry)
        
        with open(income_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return {
            'success': True,
            'message': f'Recorded {"income" if category == "revenue" else "expense"} of ${amount}',
            'entry': entry,
            'total_tracked': len(self.income_tracking)
        }
    
    def financial_report(self, period: str = 'month') -> Dict:
        """Generate financial report for side hustles"""
        print(f"[BUSINESS] Generating {period}ly financial report...")
        
        # Load all tracked data
        income_file = Path("data/income_tracking.json")
        all_entries = []
        if income_file.exists():
            with open(income_file, 'r') as f:
                all_entries = json.load(f)
        
        # Calculate totals
        total_revenue = sum(e['amount'] for e in all_entries if e['category'] == 'revenue')
        total_expenses = sum(e['amount'] for e in all_entries if e['category'] == 'expense')
        net_profit = total_revenue - total_expenses
        
        # By project
        projects = {}
        for entry in all_entries:
            proj = entry['project']
            if proj not in projects:
                projects[proj] = {'revenue': 0, 'expenses': 0}
            if entry['category'] == 'revenue':
                projects[proj]['revenue'] += entry['amount']
            else:
                projects[proj]['expenses'] += entry['amount']
        
        return {
            'success': True,
            'period': period,
            'summary': {
                'total_revenue': f'${total_revenue:.2f}',
                'total_expenses': f'${total_expenses:.2f}',
                'net_profit': f'${net_profit:.2f}',
                'profit_margin': f'{(net_profit/total_revenue*100) if total_revenue > 0 else 0:.1f}%'
            },
            'by_project': projects,
            'total_transactions': len(all_entries),
            'generated_at': datetime.now().isoformat()
        }
    
    def growth_strategies(self, project_name: str) -> Dict:
        """Provide growth strategies for an active project"""
        strategies = {
            'marketing': [
                'Leverage social media platforms consistently',
                'Start content marketing (blog, videos, podcasts)',
                'Implement referral programs',
                'Partner with complementary businesses',
                'Run targeted paid advertising campaigns'
            ],
            'product_service': [
                'Gather and implement customer feedback',
                'Add premium tiers or upsells',
                'Create bundled offerings',
                'Develop passive income products',
                'Automate delivery processes'
            ],
            'operations': [
                'Use automation tools (Zapier, IFTTT)',
                'Outsource repetitive tasks',
                'Implement CRM system',
                'Create standard operating procedures',
                'Track KPIs religiously'
            ],
            'scaling': [
                'Hire virtual assistants',
                'Build a team of freelancers',
                'Create digital products for scale',
                'License your methodology',
                'Franchise or white-label options'
            ]
        }
        
        return {
            'success': True,
            'project': project_name,
            'strategies': strategies,
            'recommended_first_steps': [
                strategies['marketing'][0],
                strategies['operations'][0],
                strategies['product_service'][0]
            ],
            'timeline_suggestion': 'Focus on one strategy per month for sustainable growth'
        }
    
    def execute_capability(self) -> Dict:
        """Return agent capabilities"""
        return {
            'agent_name': self.name,
            'capabilities': [
                'generate_side_hustle_ideas',
                'create_business_plans',
                'track_income_expenses',
                'financial_reporting',
                'growth_strategies',
                'market_analysis',
                'personalized_recommendations'
            ],
            'features': {
                'idea_generation': 'AI-powered personalized side hustle suggestions',
                'business_planning': 'Comprehensive business plans with financial projections',
                'income_tracking': 'Track revenue and expenses across projects',
                'reporting': 'Detailed financial reports and analytics',
                'growth_advice': 'Actionable strategies for scaling'
            },
            'current_profile': {
                'skills': self.user_skills,
                'interests': self.interests,
                'available_time': f'{self.available_time} hrs/week',
                'budget': f'${self.startup_budget}'
            }
        }


def estimate_monthly_expenses(business_type: str) -> Dict:
    """Estimate monthly expenses based on business type"""
    base_expenses = {
        'software_tools': 50,
        'marketing': 100,
        'hosting_domain': 20,
        'miscellaneous': 50
    }
    
    if 'tech' in business_type.lower() or 'development' in business_type.lower():
        base_expenses['software_tools'] = 100
    elif 'youtube' in business_type.lower() or 'content' in business_type.lower():
        base_expenses['software_tools'] = 75
        base_expenses['equipment_rental'] = 100
    
    return base_expenses


if __name__ == "__main__":
    # Test the Business agent
    agent = BusinessAgent()
    print("=== MIKE AI Business Agent ===\n")
    print(json.dumps(agent.execute_capability(), indent=2))
    
    # Example: Setup profile
    # agent.setup_profile(
    #     skills=['Python', 'Writing', 'Design'],
    #     interests=['AI', 'Content Creation'],
    #     available_hours=15,
    #     budget=1000
    # )
    
    # Example: Generate ideas
    # ideas = agent.generate_ideas(count=5)
    # print(json.dumps(ideas, indent=2))
