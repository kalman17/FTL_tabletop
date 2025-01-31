import random
import math

def pick_room_gaussian(center, num_rooms, stdev=1.5):
    """
    Sample an integer room number from a normal distribution
    centered on 'center', clamped to [1, num_rooms].
    """
    val = random.gauss(mu=center, sigma=stdev)
    room_candidate = round(val)
    return max(1, min(room_candidate, num_rooms))

def attack_ship_general(roll_val, attacker_mod, ship_evasion, num_rooms):
    """
    Simple version of the general shot logic.
    """
    final_roll = roll_val + attacker_mod
    print(f"Final Roll: {final_roll}")
    if final_roll < ship_evasion:
        return "Miss!"
    difference = final_roll - ship_evasion
    hit_room = (difference % num_rooms) + 1
    print(f"Hit! You strike room #{hit_room}.")
    return f"Hit! You strike room #{hit_room}."

def attack_ship_targeted(roll_val, attacker_mod, ship_evasion, num_rooms, target_room):
    """
    Targeted shot logic with priority:
      1) T_near = ship_evasion + 10
      2) T_perfect_raw = T_near + 0.2*ship_evasion
      3) near-miss band >= 5 points if possible
      4) final_roll = roll_val + attacker_mod
    """
    # 1) Baseline threshold
    T_near = ship_evasion + 10

    # 2) Perfect raw
    T_perfect_raw = T_near + 0.2 * ship_evasion

    # 3) Enforce a 5-point near-miss band
    min_perfect_with_band = T_near + 5
    if T_perfect_raw < min_perfect_with_band:
        T_perfect_raw = min_perfect_with_band

    # 4) final roll
    final_roll = roll_val + attacker_mod
    print(f"Final Roll: {final_roll}")
    print(f"T_near: {T_near}, T_perfect: {T_perfect_raw}")
    if final_roll < T_near:
        return "Miss!"
    elif final_roll < T_perfect_raw:
        drifted_room = pick_room_gaussian(center=target_room, num_rooms=num_rooms)
        if drifted_room == target_room:
            return f"Near miss by roll, but still clipped room #{target_room}!"
        return f"Near miss! Instead of room #{target_room}, you hit room #{drifted_room}."
    else:
        return f"Hit room #{target_room}!"
