import random
import os

# Dictionary mapping color numbers to emoji representations
# Empty string maps to two spaces for alignment
EMOJIS = {
    "1": "🔴", "2": "🟠", "3": "🟡", "4": "🟢", "5": "🔵",
    "6": "🟣", "7": "⚫️", "8": "⚪️", "9": "🟤", "10": "🧿",
    "": "  "
}


class Game:
    def __init__(self, size):
        """Initialize a new Bird Sort game.
        
        Args:
            size (int): Number of branches in the game (includes 2 empty branches)
        """
        self.size = size
        self.jogo = self.generate_initial_state(size)

    def generate_initial_state(self, num_branches):
        """Generate the initial game state with randomly distributed birds.
        
        The game starts with num_branches-2 colors, 4 birds of each color
        distributed randomly across num_branches-2 branches, plus 2 empty branches.
        
        Args:
            num_branches (int): Total number of branches including empty ones
            
        Returns:
            list: 2D list representing branches and their birds
        """
        # Calculate number of colors needed (2 branches will be empty)
        num_colors = num_branches - 2
        
        # Create list of colors: 4 birds of each color
        colors = [str(i + 1) for i in range(num_colors) for _ in range(4)]
        random.shuffle(colors)  # Randomly shuffle the colors

        # Initialize all branches as empty
        branches = [[""] * 4 for _ in range(num_branches)]
        
        # Fill all branches except the last two with birds
        color_index = 0
        for branch in range(num_branches - 2):
            for position in range(4):
                branches[branch][position] = colors[color_index]
                color_index += 1
                
        return branches

    def clear_screen(self):
        """Clear the terminal screen in a cross-platform way.
        
        Attempts to use system commands first (cls/clear),
        falls back to printing newlines if commands fail.
        """
        try:
            # For Windows
            if os.name == 'nt':  
                os.system('cls')
            # For Unix/Linux/MacOS
            else:  
                os.system('clear')
        except OSError:
            # Fallback: print multiple newlines
            print("\n" * 30) 

    def display_game(self):
        """Display the current game state in a two-column layout.
        
        The display shows branches numbered from 1 to N, with the first half
        on the left and the second half on the right. Each bird is represented
        by its corresponding emoji. Empty branches show nest emojis.
        """
        self.clear_screen()
        
        # Split branches into left and right columns
        total_branches = len(self.jogo)
        middle = (total_branches + 1) // 2
        left_branches = self.jogo[:middle]
        right_branches = self.jogo[middle:]

        # Calculate how many rows we need to display
        rows = max(len(left_branches), len(right_branches))
        print()  # Add some spacing at the top
        
        # Display each row
        for i in range(rows):
            # Handle left column
            if i < len(left_branches):
                left_branch = left_branches[i]
                left_number = f"{i + 1:>2} |"  # Right-aligned branch number
                left_birds = ''.join(f" {EMOJIS[c]}" for c in left_branch)
            else:
                # If we're past the left branches, show empty space
                left_number = "   |"
                left_birds = " 🪹 🪹 🪹 🪹 "  # Empty nests

            # Handle right column
            if i < len(right_branches):
                right_branch = right_branches[i]
                right_number = f"| {middle + i + 1:<2}"  # Left-aligned branch number
                right_birds = ''.join(f" {EMOJIS[c]}" for c in right_branch)
            else:
                # If we're past the right branches, show nothing
                right_number = ""
                right_birds = ""

            # Print the complete row
            if right_birds:  # If there's content for the right side
                print(f"{left_number}{left_birds}      {right_birds} {right_number}")
            else:  # If there's only content for the left side
                print(f"{left_number}{left_birds}")

    def is_right_branch(self, index):
        """Determine if a branch is in the right column of the display.
        
        Args:
            index (int): Branch index (0-based)
            
        Returns:
            bool: True if the branch is in the right column, False otherwise
        """
        middle = (self.size + 1) // 2
        return index >= middle

    def is_valid_move(self, source, destination, source_is_right, dest_is_right):
        """Check if moving birds from source to destination branch is valid.
        
        A move is valid if:
        1. Source branch is not empty
        2. Birds can be extracted from source
        3. Destination branch is either empty or has matching birds
        4. Destination branch has space for at least one bird
        
        Args:
            source (list): Source branch birds
            destination (list): Destination branch birds
            source_is_right (bool): Whether source is in right column
            dest_is_right (bool): Whether destination is in right column
            
        Returns:
            tuple: (is_valid, num_birds_to_move)
        """
        # Check if source branch is empty
        if all(bird == "" for bird in source):
            return False, 0

        # Try to extract birds from source
        movable_birds, _ = self.extract_birds(source, source_is_right, 4)
        if not movable_birds:
            return False, 0

        # Get color of birds being moved
        bird_color = movable_birds[0]

        # Check destination branch
        if all(bird == "" for bird in destination):
            # Empty destination branch can accept any color
            available_space = 4
        else:
            # Find the topmost bird in destination
            top_bird = None
            if dest_is_right:
                # For right column, scan left to right
                for bird in destination:
                    if bird != "":
                        top_bird = bird
                        break
            else:
                # For left column, scan right to left
                for bird in reversed(destination):
                    if bird != "":
                        top_bird = bird
                        break
                        
            # Colors must match
            if top_bird != bird_color:
                return False, 0
                
            # Count empty spaces in destination
            available_space = destination.count("")

        # If there's space, determine how many birds can be moved
        if available_space > 0:
            num_birds = min(len(movable_birds), available_space)
            return True, num_birds
            
        return False, 0

    def extract_birds(self, branch, is_right, max_birds):
        """Extract birds from a branch based on their position and color.
        
        For right-side branches, birds are extracted from left to right.
        For left-side branches, birds are extracted from right to left.
        Only consecutive birds of the same color can be extracted.
        
        Args:
            branch (list): The branch to extract birds from
            is_right (bool): Whether this is a right-side branch
            max_birds (int): Maximum number of birds to extract
            
        Returns:
            tuple: (extracted_birds, updated_branch)
        """
        # Create a copy of the branch to modify
        new_branch = branch[:]
        extracted_birds = []

        if is_right:
            # For right branches, start from the leftmost position
            position = 0
            # Skip empty spaces
            while position < 4 and branch[position] == "":
                position += 1
            # If branch is empty, return
            if position == 4:
                return [], branch

            # Get the color and count consecutive matching birds
            color = branch[position]
            consecutive_count = 1
            while position + consecutive_count < 4 and branch[position + consecutive_count] == color:
                consecutive_count += 1
                
            # Extract birds (limited by max_birds)
            birds_to_extract = min(consecutive_count, max_birds)
            extracted_birds = [color] * birds_to_extract
            
            # Update the branch (remove extracted birds)
            for i in range(birds_to_extract):
                new_branch[position + i] = ""
        else:
            # For left branches, start from the rightmost position
            position = 3
            # Skip empty spaces
            while position >= 0 and branch[position] == "":
                position -= 1
            # If branch is empty, return
            if position == -1:
                return [], branch

            # Get the color and count consecutive matching birds
            color = branch[position]
            consecutive_count = 1
            while position - consecutive_count >= 0 and branch[position - consecutive_count] == color:
                consecutive_count += 1
                
            # Extract birds (limited by max_birds)
            birds_to_extract = min(consecutive_count, max_birds)
            extracted_birds = [color] * birds_to_extract
            
            # Update the branch (remove extracted birds)
            for i in range(birds_to_extract):
                new_branch[position - i] = ""

        return extracted_birds, new_branch

    def insert_birds(self, branch, birds_to_insert, is_right):
        """Insert birds into a branch based on its position (left/right).
        
        For right-side branches, birds are inserted from right to left.
        For left-side branches, birds are inserted from left to right.
        
        Args:
            branch (list): The branch to insert birds into
            birds_to_insert (list): Birds to be inserted
            is_right (bool): Whether this is a right-side branch
            
        Returns:
            list: Updated branch with new birds inserted
        """
        # Create a copy of the branch to modify
        new_branch = branch[:]

        if is_right:
            # For right branches, start from rightmost position
            position = 3
            # Find the rightmost empty space
            while position >= 0 and new_branch[position] != "":
                position -= 1
            # Insert birds from right to left
            for bird in reversed(birds_to_insert):
                if position < 0:  # Stop if branch is full
                    break
                new_branch[position] = bird
                position -= 1
        else:
            # For left branches, start from leftmost position
            position = 0
            # Find the leftmost empty space
            while position < 4 and new_branch[position] != "":
                position += 1
            # Insert birds from left to right
            for bird in birds_to_insert:
                if position >= 4:  # Stop if branch is full
                    break
                new_branch[position] = bird
                position += 1

        return new_branch

    def is_game_solved(self):
        """Check if the game is solved.
        
        The game is solved when:
        1. Each non-empty branch contains birds of only one color
        2. Each branch is either completely full (4 birds) or completely empty
        
        Returns:
            bool: True if game is solved, False otherwise
        """
        for branch in self.jogo:
            # Get unique colors in this branch (excluding empty spaces)
            colors = set(bird for bird in branch if bird != "")
            
            # Check if branch violates solution conditions:
            # - More than one color in the branch, or
            # - Branch is partially filled (not empty or full)
            if len(colors) > 1 or branch.count("") not in [0, 4]:
                return False
                
        return True
