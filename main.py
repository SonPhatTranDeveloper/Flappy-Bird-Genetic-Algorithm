import sys

from pygame.sprite import Group

from objects import Background, Pipes, BigText, SmallText
from objects.bird_flock import BirdFlock
from init import *
from config import GAME_FPS


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None

        # Initialize the game objects
        self.bird_flock = BirdFlock()
        self.background = Background()
        self.generation_text = None
        self.survival_text = None
        self.max_score_text = None

        # Keep track of an array of pipes
        self.pipes = []

        # Add top sprites
        self.all_sprites = Group()
        self.all_sprites.add(self.background)
        self.all_sprites.add(*self.pipes)
        self.all_sprites.add(*self.bird_flock.get_birds())

    def on_init(self):
        self._display_surf = DISPLAY_SURFACE
        self._running = True

    def on_event(self, event):
        # Check quit game
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        # Remove pipes and birds
        self.remove_pipes()
        self.remove_birds(self.pipes)

        # Generate pipe
        self.generate_pipe()

        # Check bird state
        if self.bird_flock.is_all_dead(self.pipes):
            self.restart()

        # Increase the score of the surviving birds
        self.bird_flock.increase_score()

        # Move the bird
        self.bird_flock.move()

        # Check if bird should move
        self.bird_flock.make_decision(self.pipes)

        # Change text
        self.change_generation_text(self.bird_flock.current_generation)
        self.change_survival_text(self.bird_flock.current_survival_time // 60)
        self.change_max_score_text(self.bird_flock.all_time_max_survival_time // 60)

        # Move the pipe
        for pipe in self.pipes:
            pipe.move()

    def on_render(self):
        # Draw all the sprites
        for sprite in self.all_sprites:
            if type(sprite) is Pipes:
                self._display_surf.blit(sprite.first_pipe, sprite.first_rect)
                self._display_surf.blit(sprite.second_pipe, sprite.second_rect)
            else:
                self._display_surf.blit(sprite.surf, sprite.rect)

        # Update
        pygame.display.update()
        FRAME_PER_SEC.tick(GAME_FPS)

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def remove_pipes(self):
        """
        Remove pipes that are out-of-screen
        :return: None
        """
        # Remove pipes
        if len(self.pipes) > 0:
            # Get the first pipe
            first_pipe = self.pipes[0]

            # Check if invalid
            if first_pipe.first_rect.right <= 0:
                self.all_sprites.remove(first_pipe)
                self.pipes.pop(0)

    def remove_birds(self, pipes):
        for bird in self.bird_flock.get_birds():
            if bird.is_dead(pipes):
                self.all_sprites.remove(bird)

    def generate_pipe(self):
        """
        Generate new pipes
        :return: None
        """
        # Generate pipes
        if len(self.pipes) < 2:
            new_pipes = Pipes.generate_pipes()
            for new_pipe in new_pipes:
                self.pipes.append(new_pipe)
                self.all_sprites.add(new_pipe)

    def restart(self):
        """
        Restart the game
        :return: None
        """
        self._running = True

        # Evolve the bird population
        self.bird_flock.evolve()

        # Initialize the game objects
        self.background = Background()

        # Keep track of an array of pipes
        self.pipes = []

        # Remove all previous sprites
        self.all_sprites.clear(DISPLAY_SURFACE, self.background.surf)

        # Add top sprites
        self.all_sprites = Group()
        self.all_sprites.add(self.background)
        self.all_sprites.add(*self.pipes)
        self.all_sprites.add(*self.bird_flock.get_birds())

    def change_generation_text(self, generation: int):
        # Remove previous text
        if self.generation_text:
            self.all_sprites.remove(self.generation_text)

        # Create text
        self.generation_text = BigText(f"Generation: {generation}")
        self.generation_text.rect.center = (GAME_WIDTH / 2, 50)

        # Draw to screen
        self.all_sprites.add(self.generation_text)

    def change_survival_text(self, survival_time: int):
        # Remove previous text
        if self.survival_text:
            self.all_sprites.remove(self.survival_text)

        # Create text
        self.survival_text = SmallText(f"Time: {survival_time} (s)")
        self.survival_text.rect.center = (GAME_WIDTH / 2, 90)

        # Draw to screen
        self.all_sprites.add(self.survival_text)

    def change_max_score_text(self, survival_time: int):
        # Remove previous text
        if self.max_score_text:
            self.all_sprites.remove(self.max_score_text)

        # Create text
        self.max_score_text = SmallText(f"Max: {survival_time} (s)")
        self.max_score_text.rect.center = (GAME_WIDTH / 2, 120)

        # Draw to screen
        self.all_sprites.add(self.max_score_text)



if __name__ == "__main__":
    app = App()
    app.on_execute()

