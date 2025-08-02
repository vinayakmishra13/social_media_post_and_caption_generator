"""Social_media_post_and_caption_generator.py

### Install Required Libraries
Install the necessary Python packages like `transformers`and `gradio`.
"""

!pip install transformers gradio

"""### Import Libraries and Initialize
Import `gradio`, `transformers`, and `random` for UI, model, and utility functions.
"""

import gradio as gr
from transformers import pipeline
import random

"""### Initialize Text Generation Model
Set up the GPT-2 model for generating social media captions.
"""

caption_generator=pipeline("text-generation",model="gpt2")

"""### Define Emoji Generator
Use sentiment analysis to determine mood and return corresponding emojis.
"""

emoji_dict={
    "positive": ["😊","🌟","🔥","💪","🚀","✨"],
    "negative":["😢","😞","💔","😠","😓"],
    "neutral":["🙂","😐","🧐","🤔","😶"]
}


sentiment_pipeline=pipeline("sentiment-analysis")


def get_emojis(text):
  label=sentiment_pipeline(text)[0]['label'].lower()
  return''.join(random.sample(emoji_dict.get(label,["😐"]),3))

"""### Hashtag Generator Function
Create relevant hashtags based on input prompt and selected platform.
"""

def get_hashtags(prompt, platform):
  words=prompt.lower().split()
  tags=["#" + word.replace(" ","")for word in words if len(word)>3]


  platform_tags={
      "Instagram":["#instadaily","#igers","#pipcoftheday"],
      "LinkedIn":["#career","#leadership","#networking"],
      "Twitter":["#tweet","#trending","#news"]
  }
  return" ".join(tags[:5]+ random.sample(platform_tags[platform],2))

"""### Define Caption Generation Function
Generate a complete social media caption with emojis and hashtags.
"""

def generate_post(prompt, platform):
  #Generate caption
  caption = caption_generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']


  #Generate emojis
  emojis=get_emojis(caption)


  #Generate hashtags
  hashtags = get_hashtags(prompt, platform)


  return caption.strip(), emojis, hashtags

"""###  Launch Gradio Interface
Build and launch the Gradio UI for user input and output display.
"""

interface = gr.Interface(
    fn=generate_post,
    inputs=[
         gr.Textbox(label="Enter keyword or theme"),
        gr.Radio(["Instagram", "LinkedIn", "Twitter"],label="Choose Platform")
        ],
    outputs=[
        gr.Textbox(label="Generated Caption"),
        gr.Textbox(label="Emojis"),
        gr.Textbox(label="Hashtags")
    ],
    title="Social Media Post & Caption Generator",
    description="Generate catchy captions, relevent hashtags, and emojis based on your theme!"
    )



interface.launch()
