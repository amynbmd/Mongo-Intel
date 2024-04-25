// In src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import '../Style/Home.css';

function Home() {
    return (
        <div className="home-container">
            <section className="hero-section">
                <h1>Welcome to Mongo Intel</h1>
                <p>Explore comprehensive tracking and analysis tools</p>
            </section>

            <section className="features-section">
                <h2>Our Features</h2>
                <div className="features">
                    {/* Feature blocks */}
                    <div className="feature">
                        <h3>Predictive Analysis</h3>
                        <p>Predict future trends from historical data.</p>
                        <Link to="/area-analysis">Learn More</Link>
                    </div>
                    <div className="feature">
                        <h3>Area Analysis</h3>
                        <p>Analyze geographical data over specific areas.</p>
                        <Link to="/predictive-analysis">Learn More</Link>
                    </div>
                    <div className="feature">
                        <h3>Chatbot Platform</h3>
                        <p>Provide a user-friendly interface for interacting with AI technology, offering insightful answers.</p>
                        <Link to="/real-time-tracking">Learn More</Link>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
