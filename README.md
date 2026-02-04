# Real-Time Speech-to-Sign Language Translation System

A real-time Speech-to-Sign Language Translation system that converts spoken language into structured text using Whisper ASR and maps it to sign-language gestures using an NLP processing pipeline and Streamlit interface.

---

## Overview

This project implements an end-to-end pipeline for converting live speech into sign-language gesture outputs. It combines Automatic Speech Recognition (ASR), Natural Language Processing (NLP), and a real-time visualization interface.

The system is designed to support accessibility-focused communication using modular and extensible ML components.

---

## Pipeline Architecture

Speech Input → Whisper ASR → Text Processing → NLP Tokenization & POS Tagging → Gesture Mapping → Streamlit Interface Output

---

## Key Features

- Real-time speech recognition using Whisper ASR
- NLP pipeline for tokenization and POS tagging
- Structured token mapping to sign-language gesture database
- Context-aware text preprocessing
- Streamlit-based multilingual user interface
- Modular ASR → NLP → Gesture mapping workflow
- Designed for extensibility and dataset expansion

---

## Tech Stack

- Python
- Whisper ASR
- NLP (tokenization, POS tagging)
- Streamlit
- Text preprocessing libraries

---

## Project Structure (Planned)

src/ — core pipeline code  
notebooks/ — experiments and testing  
data/ — gesture mapping resources  
outputs/ — demo outputs and samples  
screenshots/ — UI and pipeline screenshots  

---

## Use Cases

- Accessibility communication support
- Speech-to-sign assistive tools
- Real-time gesture translation systems
- NLP + ASR integration projects

---

## Status

Academic ML project with working prototype pipeline and interface.
