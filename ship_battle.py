import random
import math

def main():
    """
    Main menu loop.
    """
    while True:
        print("\n=== MAIN MENU ===")
        print("1) Start new battle")
        print("2) Quit")
        choice = input("Choice: ").strip()

        if choice == "1":
            start_battle()
        elif choice == "2":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

def start_battle():
    """
    Set up the enemy ship stats and begin a turn-by-turn sequence of player shots.
    (Extend later with enemy AI, multiple ships, etc.)
    """
    print("\n--- NEW BATTLE SETUP ---")

    # Gather basic enemy ship data
    try:
        ship_evasion = int(input("Enemy ship Evasion %: ").strip())
        num_rooms = int(input("Number of rooms in enemy ship: ").strip())
        enemy_hull = int(input("Enemy Hull (HP): ").strip())
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return

    # For simplicity, the player might have a single 'attack modifier'
    try:
        attacker_mod = int(input("Enter your attack modifier (gunner skill + weapon accuracy): ").strip())
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return

    # Default penalty for targeted shots (can adjust to taste)
    targeting_penalty = 25

    turn_count = 1

    # Main battle loop
    while enemy_hull > 0:
        print(f"\n=== TURN {turn_count} ===")
        print(f"Enemy Hull: {enemy_hull}")
        print("Choose your firing mode:")
        print("1) General shot (hit any room)")
        print("2) Targeted shot (-25%% accuracy penalty)")
        print("3) Quit battle")
        choice = input("Choice: ").strip()

        if choice == "1":
            # General shot
            roll_mode = input("Auto-roll (a) or manual input (m)? ").lower().strip()
            if roll_mode.startswith('m'):
                try:
                    roll_val = int(input("Enter your d100 roll: ").strip())
                except ValueError:
                    print("Invalid roll input. No shot this turn.")
                    turn_count += 1
                    continue
            else:
                roll_val = random.randint(1, 100)

            result = attack_ship_general(roll_val, attacker_mod, ship_evasion, num_rooms)
            if "Miss" in result:
                print(result)
            else:
                # For demonstration, we do 1 hull damage on a hit
                print(result)
                enemy_hull -= 1

        elif choice == "2":
            # Targeted shot
            try:
                target_room = int(input(f"Which room do you want to target? (1..{num_rooms}): ").strip())
                if target_room < 1 or target_room > num_rooms:
                    raise ValueError
            except ValueError:
                print("Invalid room choice. No shot this turn.")
                turn_count += 1
                continue

            roll_mode = input("Auto-roll (a) or manual input (m)? ").lower().strip()
            if roll_mode.startswith('m'):
                try:
                    roll_val = int(input("Enter your d100 roll: ").strip())
                except ValueError:
                    print("Invalid roll input. No shot this turn.")
                    turn_count += 1
                    continue
            else:
                roll_val = random.randint(1, 100)

            result = attack_ship_targeted(
                roll_val=roll_val,
                attacker_mod=attacker_mod,
                ship_evasion=ship_evasion,
                num_rooms=num_rooms,
                target_room=target_room,
                targeting_penalty=targeting_penalty
            )
            if "Miss" in result:
                print(result)
            else:
                # For demonstration, 1 hull damage
                print(result)
                enemy_hull -= 1

        elif choice == "3":
            print("Retreating from battle...")
            break
        else:
            print("Invalid choice.")

        turn_count += 1

    if enemy_hull <= 0:
        print("\n*** The enemy ship is defeated! ***")

# --------------------------------------------------------------------------
# 1) GENERAL SHOT LOGIC (no adjacency, just random room on a hit)
# --------------------------------------------------------------------------
def attack_ship_general(roll_val, attacker_mod, ship_evasion, num_rooms):
    """
    Perform a general shot:
    - finalRoll = roll_val + attacker_mod
    - Compare vs. ship_evasion
    - If fail => "Miss"
    - Else => pick a random room based on (finalRoll - shipEvasion) mod num_rooms
    """
    final_roll = roll_val + attacker_mod
    if final_roll < ship_evasion:
        return f"Miss! (Roll total {final_roll} < Evasion {ship_evasion})"

    difference = final_roll - ship_evasion
    # "roomIndex" is 0..(num_rooms-1)
    room_index = difference % num_rooms
    hit_room = room_index + 1
    return f"Hit! You strike room #{hit_room}."

# --------------------------------------------------------------------------
# 2) TARGETED SHOT LOGIC (with Gaussian drift if close miss)
# --------------------------------------------------------------------------
def attack_ship_targeted(roll_val, attacker_mod, ship_evasion,
                         num_rooms, target_room, targeting_penalty=25):
    """
    Targeted shot process:
      1) finalRoll = roll_val + attacker_mod - targeting_penalty
      2) If finalRoll >= ship_evasion -> direct hit on target_room
      3) Else, see margin = ship_evasion - finalRoll
          - if margin > 10 => total miss
          - else => "near miss": pick a nearby room using a Gaussian
                    distribution centered on target_room
    Returns a string describing the result.
    """
    final_roll = roll_val + attacker_mod - targeting_penalty
    if final_roll >= ship_evasion:
        # Direct hit on the chosen room
        return f"Success! You precisely hit the targeted room #{target_room}."

    # We missed the threshold
    margin = ship_evasion - final_roll
    if margin > 10:
        # Miss entirely
        return f"Miss! (Failed by {margin} > 10)"

    # If we missed by 10 or less, we do a Gaussian drift around 'target_room'
    # (means we shot close but not perfect)

    drifted_room = pick_room_gaussian(center=target_room, num_rooms=num_rooms, stdev=1.7)
    return f"Near miss! Instead of room #{target_room}, you hit room #{drifted_room}."

# --------------------------------------------------------------------------
# GAUSSIAN HELPER
# --------------------------------------------------------------------------
def pick_room_gaussian(center, num_rooms, stdev=1.5):
    """
    Sample an integer room number from a normal distribution
    with mean = center, standard deviation = stdev,
    clamped to [1, num_rooms].
    """
    # We'll draw until we get a valid 1..num_rooms (or just clamp).
    while True:
        val = random.gauss(mu=center, sigma=stdev)
        # Round to nearest integer
        room_candidate = round(val)
        # Clamp to 1..num_rooms
        if room_candidate < 1:
            room_candidate = 1
        elif room_candidate > num_rooms:
            room_candidate = num_rooms
        return room_candidate

# Run the main menu if executed directly
if __name__ == "__main__":
    main()
