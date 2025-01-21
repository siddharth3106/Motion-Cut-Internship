def count_words(text):
    """
    Count the number of words in the given text.
    
    Parameters:
        text (str): The input text.
    
    Returns:
        int: The number of words in the text.
    """
    # Split the text by whitespace to get a list of words
    words = text.split()
    return len(words)

def main():
    """
    Main function to handle user input, word counting, and output display.
    """
    print("Welcome to the Word Counter Program!")
    print("Enter your text below to count the number of words.")
    print("-------------------------------------------------")

    # Prompt the user to enter a sentence or paragraph
    user_input = input("Please enter your text: ").strip()

    # Error Handling: Check for empty input
    if not user_input:
        print("Error: You entered an empty input. Please try again!")
        return

    # Call the word counting function
    word_count = count_words(user_input)

    # Display the output
    print("\nWord Count Result:")
    print(f"The total number of words in your text is: {word_count}")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
