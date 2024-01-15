import openai
import time

# Set your OpenAI API key
openai.api_key = "API_KEY"

def generate_response(conversation_history):
    try:
        # Make a request to the OpenAI API with GPT-3.5 Turbo for chat
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # GPT-3.5 Turbo model
            messages=conversation_history,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError as e:
        # Handle rate limit error by waiting and then retrying
        wait_time = int(e.headers['Retry-After']) + 1  # Add an extra second to be safe
        print(f"Rate limit reached. Waiting for {wait_time} seconds.")
        time.sleep(wait_time)
        return generate_response(conversation_history)

def chat_with_gpt(input_list):
    conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

    for user_input in input_list:
        # Append user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Generate a response from ChatGPT
        response = generate_response(conversation_history)

        # Append ChatGPT's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

    s = " for all pieces of code one by one in the repository I told you about in my first prompt and provided code for."
    predefined_options = [
        "Provide insights and suggestions on the codebase",
        "Enhance code quality and maintainability. Suggestions for code refactoring and improvements",
        "Improve code performance. Identifying areas for efficiency increase, such as reducing time complexity",
        "Strengthen testing and validation. Suggest additional test cases for better coverage",
        "Identify and fix potential bugs. Pinpointing bugs with possible solutions or preventive measures"
    ]

    while True:
        print("\nAsk anything about the repository now.")
        print("Type the number corresponding to the predefined option or ask your own question.")

        for idx, option in enumerate(predefined_options, start=1):
            print(f"{idx}. {option}")

        user_input = input("Your choice (type 'exit' to stop): ")

        if user_input.lower() == 'exit':
            break

        try:
            user_choice = int(user_input)
            if 1 <= user_choice <= len(predefined_options):
                user_question = predefined_options[user_choice - 1] + s
            else:
                raise ValueError()
        except ValueError:
            user_question = input("Your own question: ")

        conversation_history.append({"role": "user", "content": user_question})

        # Generate a response from ChatGPT
        response = generate_response(conversation_history)

        # Display the response
        print(f"ChatGPT: {response}")

        # Append ChatGPT's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    # Input a list of user inputs
    input_list = [
        "What is the purpose of the repository?",
        "How can I contribute?",
        # Add more inputs as needed
    ]

    chat_with_gpt(input_list)
