from objects.bird import Bird
from ai.genetic_engine import breed_bird, clone_bird


class BirdFlock:
    def __init__(self, num_birds=600):
        # Save the current number of birds
        self.num_birds = num_birds

        # Create the initial birds
        self.birds = [Bird() for _ in range(num_birds)]

        # Save the current number of generation
        self.current_generation = 1

        # Save the current survival time
        self.current_survival_time = 0
        self.all_time_max_survival_time = 0

        # Save the best bird
        self.best_bird = None

    def get_birds(self):
        return self.birds

    def is_all_dead(self, pipes):
        for bird in self.birds:
            bird.is_dead(pipes)
            if not bird.dead:
                return False

        return True

    def move(self):
        for bird in self.birds:
            if not bird.dead:
                bird.move()

    def make_decision(self, pipes):
        for bird in self.birds:
            if not bird.dead:
                bird.make_decision(pipes)

    def increase_score(self):
        for bird in self.birds:
            if not bird.dead:
                # Calculate bird score
                bird.increase_score()

                # Update time
                self.current_survival_time = max(self.current_survival_time, bird.score)
                self.all_time_max_survival_time = max(self.all_time_max_survival_time, self.current_survival_time)

                # Get the best bird of all the generations
                if bird.score >= self.all_time_max_survival_time:
                    self.best_bird = bird

    def evolve(self):
        """
        Evolve the bird flock to the next generation
        :return: None
        """
        # Increase the number of generation
        self.current_generation += 1

        # Reset survival time
        self.current_survival_time = 0

        # Choose the two birds with the highest score
        self.birds.sort(key=lambda bird: bird.score, reverse=True)
        bird_mom, bird_dad = self.birds[:2]

        # Set the current generation and clone the bird mom and bird dad to the current generation
        self.birds = (breed_bird(bird_mom, bird_dad, num_children=self.num_birds // 6)
                      + clone_bird(bird_mom, num_children=self.num_birds // 6)
                      + clone_bird(bird_dad, num_children=self.num_birds // 6)
                      + clone_bird(self.best_bird, num_children=self.num_birds // 6)
                      + [bird_mom.clone() for _ in range(self.num_birds // 6)]
                      + [self.best_bird.clone() for _ in range(self.num_birds // 6)])