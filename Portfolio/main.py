from website import create_app

# Run the Flask app in debug mode
app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode