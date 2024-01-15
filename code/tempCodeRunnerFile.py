      if transitioning:
                if self.stop is None:
                    self.stop = self.start_x + TRANSITION_DISTANCE if self.action == retour else self.start_x - TRANSITION_DISTANCE
                if (self.action == retour and self.x < self.stop) or (self.action != retour and self.x > self.stop):
                    self.x += TRANSITION_SPEED if self.action == retour else -TRANSITION_SPEED
                else:
                    self.x = self.stop