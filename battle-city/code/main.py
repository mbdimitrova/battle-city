from .level import initialize_level
import pygame

def main():
    """Add states to control here."""
    pygame.display.set_caption('Battle City')
    initialize_level("level01")
