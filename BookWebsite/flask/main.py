from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Dictionnaire des recommandations de livres par catégorie
BOOK_RECOMMENDATIONS = {
    "finance": [
        {"title": "Rich Dad Poor Dad", "author": "Robert T. Kiyosaki"},
        {"title": "The Intelligent Investor", "author": "Benjamin Graham"},
        {"title": "Think and Grow Rich", "author": "Napoleon Hill"},
        {"title": "The Psychology of Money", "author": "Morgan Housel"},
        {"title": "The Total Money Makeover", "author": "Dave Ramsey"},
        {"title": "The Little Book of Common Sense Investing", "author": "John C. Bogle"},
        {"title": "The Richest Man in Babylon", "author": "George S. Clason"},
        {"title": "The Simple Path to Wealth", "author": "JL Collins"},
        {"title": "The Millionaire Fastlane", "author": "M.J. DeMarco"},
        {"title": "Money: Master the Game", "author": "Tony Robbins"}
    ],
    "business": [
        {"title": "Good to Great", "author": "Jim Collins"},
        {"title": "Zero to One", "author": "Peter Thiel"},
        {"title": "Start with Why", "author": "Simon Sinek"},
        {"title": "The Lean Startup", "author": "Eric Ries"},
        {"title": "Built to Last", "author": "Jim Collins"},
        {"title": "The E-Myth Revisited", "author": "Michael E. Gerber"},
        {"title": "Blue Ocean Strategy", "author": "W. Chan Kim"},
        {"title": "The 4-Hour Work Week", "author": "Timothy Ferriss"},
        {"title": "Rework", "author": "Jason Fried"},
        {"title": "The Hard Thing About Hard Things", "author": "Ben Horowitz"}
    ],
    "psychology": [
        {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman"},
        {"title": "Man's Search for Meaning", "author": "Viktor E. Frankl"},
        {"title": "The Power of Habit", "author": "Charles Duhigg"},
        {"title": "Quiet", "author": "Susan Cain"},
        {"title": "Influence", "author": "Robert Cialdini"},
        {"title": "Mindset", "author": "Carol S. Dweck"},
        {"title": "Flow", "author": "Mihaly Csikszentmihalyi"},
        {"title": "Emotional Intelligence", "author": "Daniel Goleman"},
        {"title": "The Body Keeps the Score", "author": "Bessel van der Kolk"},
        {"title": "Atomic Habits", "author": "James Clear"}
    ],
    "investment": [
        {"title": "A Random Walk Down Wall Street", "author": "Burton Malkiel"},
        {"title": "Common Stocks and Uncommon Profits", "author": "Philip Fisher"},
        {"title": "The Little Book of Value Investing", "author": "Christopher H. Browne"},
        {"title": "One Up On Wall Street", "author": "Peter Lynch"},
        {"title": "The Essays of Warren Buffett", "author": "Warren Buffett"},
        {"title": "Security Analysis", "author": "Benjamin Graham"},
        {"title": "The Warren Buffett Way", "author": "Robert Hagstrom"},
        {"title": "Value Investing", "author": "Bruce Greenwald"},
        {"title": "The Little Book That Beats the Market", "author": "Joel Greenblatt"},
        {"title": "The Dhandho Investor", "author": "Mohnish Pabrai"}
    ],
    "leadership": [
        {"title": "Leaders Eat Last", "author": "Simon Sinek"},
        {"title": "The 21 Irrefutable Laws of Leadership", "author": "John C. Maxwell"},
        {"title": "Extreme Ownership", "author": "Jocko Willink"},
        {"title": "Good to Great", "author": "Jim Collins"},
        {"title": "Dare to Lead", "author": "Brené Brown"},
        {"title": "The 7 Habits of Highly Effective People", "author": "Stephen Covey"},
        {"title": "Emotional Intelligence 2.0", "author": "Travis Bradberry"},
        {"title": "Drive", "author": "Daniel H. Pink"},
        {"title": "Primal Leadership", "author": "Daniel Goleman"},
        {"title": "The Five Dysfunctions of a Team", "author": "Patrick Lencioni"}
    ],
    "motivation": [
        {"title": "Can't Hurt Me", "author": "David Goggins"},
        {"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson"},
        {"title": "Grit", "author": "Angela Duckworth"},
        {"title": "Mindset", "author": "Carol S. Dweck"},
        {"title": "The Power of Now", "author": "Eckhart Tolle"},
        {"title": "You Are a Badass", "author": "Jen Sincero"},
        {"title": "The Alchemist", "author": "Paulo Coelho"},
        {"title": "Think and Grow Rich", "author": "Napoleon Hill"},
        {"title": "The Mountain Is You", "author": "Brianna Wiest"},
        {"title": "Atomic Habits", "author": "James Clear"}
    ]
}

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

def get_html_template(name, topics):
    # Obtenir les recommandations pour chaque topic sélectionné
    all_recommendations = []
    for topic in topics:
        if topic.lower() in BOOK_RECOMMENDATIONS:
            all_recommendations.append({
                'topic': topic,
                'books': BOOK_RECOMMENDATIONS[topic.lower()]
            })

    # Créer le HTML pour les recommandations
    recommendations_html = ""
    for rec in all_recommendations:
        books_html = ""
        for i, book in enumerate(rec['books']):
            books_html += f'''
                <div class="book-item">
                    <strong>{i+1}. {book["title"]}</strong><br>
                    <em>by {book["author"]}</em>
                </div>
            '''
        
        recommendations_html += f'''
            <div class="topic-section">
                <h3>Top 10 {rec['topic']} Books:</h3>
                <div class="books-list">
                    {books_html}
                </div>
            </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #0f33ff;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 0 0 5px 5px;
            }}
            .topics {{
                background-color: #fff;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .topic-section {{
                margin: 20px 0;
                padding: 15px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .books-list {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
                margin-top: 10px;
            }}
            .book-item {{
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border-left: 4px solid #0f33ff;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Personalized Book Recommendations</h1>
            </div>
            <div class="content">
                <h2>Hello {name},</h2>
                <p>Thank you for using Discover Your Perfect Reads! Based on your interests, we've curated the following book recommendations just for you.</p>
                
                <div class="topics">
                    <h3>Your Selected Topics:</h3>
                    <ul>
                        {''.join(f'<li>{topic}</li>' for topic in topics)}
                    </ul>
                </div>
                
                {recommendations_html}
                
                <p>Happy reading!</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>Discover Your Perfect Reads Team</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        print("Received request")
        data = request.get_json()
        print("Request data:", data)
        
        if not all(key in data for key in ['name', 'email', 'topics']):
            return jsonify({"error": "Missing required fields"}), 400
        
        name = data['name']
        email = data['email']
        topics = data['topics']

        if not name or not email or not topics:
            return jsonify({"error": "All fields are required"}), 400

        print(f"Preparing email for {email}")

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your Personalized Book Recommendations"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email

        text_content = f"""
        Hello {name},
        
        Thank you for using Discover Your Perfect Reads!
        
        Your selected topics: {', '.join(topics)}
        
        Please check the HTML version of this email for your personalized book recommendations.
        
        Best regards,
        Discover Your Perfect Reads Team
        """
        
        html_content = get_html_template(name, topics)

        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        print("Connecting to SMTP server")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print("Logging in to SMTP server")
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Sending email")
            server.send_message(msg)
            print("Email sent successfully")

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        print(f"Error in send_email: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
