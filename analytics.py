import matplotlib.pyplot as plt

def save_price_trend(prices):
    plt.figure(figsize=(10, 5))
    plt.plot(prices, marker='o', linestyle='-', color='b', label='Delivery Price ($)')
    plt.title('Delivery Price Trend Analysis')
    plt.xlabel('Order Sequence')
    plt.ylabel('Price in USD')
    plt.grid(True)
    plt.legend()
    plt.savefig('price_trend.png')
    print("Trend graph saved as 'price_trend.png'")