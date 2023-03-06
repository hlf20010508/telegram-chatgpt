import os
import openai

class ChatGPT:
  def __init__(self, api_key, model="gpt-3.5-turbo", preset='', memory_length=100):
    openai.api_key = api_key
    self.model = model
    # 对话历史记录
    self.conversation = []
    # 一段对角色预设的描述
    self.preset = preset
    # 对话记录长度
    self.memory_length = memory_length

    self.conversation.append({
      "role": "system",
      "content": self.preset
    })

  def reply(self, message):
    self.conversation.append({
      "role": "user",
      "content": message
    })

    result = openai.ChatCompletion.create(
      model=self.model, 
      messages=self.conversation
    )
    result = result['choices'][0]['message']['content'].strip()

    self.conversation.append({
      "role": "assistant",
      "content": result
    })

    self.recycle_memory()

    return result
  
  def delete_memory(self):
    self.conversation = []
  
  # 遗忘超过设定对话记录长度的对话
  def recycle_memory(self):
    length = len(self.conversation)
    if length >= self.memory_length:
      self.conversation = self.conversation[length - self.memory_length : ]

  # 设定新的角色预设。这会清空所有对话记录
  def reset_character(self, setting):
    self.preset = setting
    self.delete_memory()
    self.conversation.append({
      "role": "system",
      "content": self.preset
    })