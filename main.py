import openai
import os
import json
import time

openai.api_key = "YOUR_API_KEY_HERE"

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def generate_ethical_dilemma_gpt4(): 
    ethical_dilemma_prompt = "Ask what would I do in the situation you generate? "
    ethical_dilemma_system_content = "Generate a short and random ethical dilemma."
    ethical_dilemma = generate_chatbot_response(ethical_dilemma_prompt, ethical_dilemma_system_content)
    return ethical_dilemma

egoist_system_content = read_file_content('Prompt Text Files/EgoistDAN.txt')
hedonist_system_content = read_file_content('Prompt Text Files/HedonisticDAN.txt')
naturalist_system_content = read_file_content('Prompt Text Files/NaturalistDAN.txt')
virtue_theorist_system_content = read_file_content('Prompt Text Files/VirtueTheoristDAN.txt')
existentialist_system_content = read_file_content('Prompt Text Files/ExistentialistDAN.txt')
kantianist_system_content = read_file_content('Prompt Text Files/KantianistDAN.txt')
utilitarianist_system_content = read_file_content('Prompt Text Files/UtilitarianistDAN.txt')
religious_system_content = read_file_content('Prompt Text Files/ReligiousDAN.txt')
judge_system_content = read_file_content('Prompt Text Files/MasterDAN.txt')


def generate_chatbot_response(prompt, system_content, retries=30, backoff_factor=2):
    for retry_count in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
                max_tokens=1200,
                n=1,
                stop=None,
                temperature=1,
            )
            return response.choices[0].message['content'].strip()
        except openai.error.OpenAIError as e:
            if 'Model overloaded' in str(e) and retry_count < retries - 1:
                sleep_time = backoff_factor ** (retry_count + 1)
                time.sleep(sleep_time)
            else:
                raise

def ethics_training_simulation():
    chatbot_1_name = "Egoist"
    chatbot_2_name = "Hedonist"
    chatbot_3_name = "Naturalist"
    chatbot_4_name = "VirtueTheorist"
    chatbot_5_name = "Existentialist"
    chatbot_6_name = "Kantianist"
    chatbot_7_name = "Utilitarianist"
    chatbot_8_name = "Religious"

    user_input = input("Please input a difficult ethical dilemma or scenario (press Enter for a random dilemma): ")
    subject = user_input.strip()
    
    if not subject:
        subject = generate_ethical_dilemma_gpt4()
        print(f"\nGenerated Ethical Dilemma: {subject}")

    conversation_history = []

    chatbot_names = [chatbot_1_name, chatbot_2_name, chatbot_3_name, chatbot_4_name, chatbot_5_name, chatbot_6_name, chatbot_7_name, chatbot_8_name]
    chatbot_system_contents = [egoist_system_content, hedonist_system_content, naturalist_system_content, virtue_theorist_system_content, existentialist_system_content, kantianist_system_content, utilitarianist_system_content, religious_system_content]

    for name, system_content in zip(chatbot_names, chatbot_system_contents):
        prompt = f"{subject} {name}: Please provide your perspective on the question."
        chatbot_response = generate_chatbot_response(prompt, system_content)
        conversation_history.append(f"{name}: {chatbot_response}")
        print(f"\n{name}: {chatbot_response}")


    final_decision = make_decision(conversation_history)
    print(f"\nMaster's Final Decision: {final_decision}")

def make_decision(conversation_history):
    judge_system_content =    prompt = f"{' '.join(conversation_history)} Master: Based on the perspectives of the chatbots, what would be the most ethical/moral decision in this situation? Speak in the first person, for example, use 'I would...' or 'I would not...' to describe what you would do in the given scenerio."

    final_decision = generate_chatbot_response(prompt, judge_system_content)
    return final_decision

if __name__ == "__main__":
    ethics_training_simulation()

