
/* Page-specific styles for history page */
.main-content {
    background: linear-gradient(135deg, #FFE5E5 0%, #FFF0F0 100%);
    min-height: 100vh;
    padding: 30px;
}

.header {
    text-align: center;
    padding: 40px 30px;
    background: linear-gradient(135deg, #FF5F5F 0%, #FF3838 100%);
    border-radius: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(255, 56, 56, 0.3);
}

/* Mobile: Use container styling */
@media screen and (max-width: 768px) {
    .main-content {
        padding: 20px;
    }
    
    .header {
        padding: 30px 20px;
        margin-bottom: 30px;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}

@media screen and (max-width: 480px) {
    .stats-grid {
        grid-template-columns: 1fr;
        gap: 15px;
    }
}

.header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    color: white;
    margin-bottom: 10px;
}

.header p {
    color: rgba(255, 255, 255, 0.9);
    font-size: 16px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
    margin-bottom: 40px;
}

.stat-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.stat-emoji {
    font-size: 40px;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #FF3838;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 14px;
    color: #666;
    font-weight: 500;
}

.chart-section {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    margin-bottom: 40px;
}

.chart-title {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin-bottom: 20px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.chart-icon {
    font-size: 28px;
}

.chart-wrapper {
    position: relative;
    height: 400px;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #999;
}

.empty-state-icon {
    font-size: 64px;
    margin-bottom: 20px;
}

.empty-state p {
    font-size: 18px;
    margin-bottom: 10px;
}

.back-btn {
    display: inline-block;
    padding: 15px 30px;
    background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
    color: white;
    text-decoration: none;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
}

.back-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(212, 175, 55, 0.5);
}

.bottom-nav {
    text-align: center;
    margin-top: 30px;
}

@media (max-width: 768px) {
    .header h1 {
        font-size: 32px;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .chart-wrapper {
        height: 300px;
    }
}