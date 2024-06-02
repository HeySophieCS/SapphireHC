from util.objects import *
from util.routines import *
from util.tools import *

class Bot(CheeseAgent):
    def run(agent):
        def drive_to(vec):
            defaultThrottle(agent, cap(agent.me.location.dist(vec) - 300, 0, 2300))
            defaultPD(agent, agent.me.local(vec - agent.me.location))

        home = agent.friend_goal.location - Vector3(0, side(agent.team)*300, 100)
        leftfield = Vector3(-side(agent.team)*4200, agent.ball.location.y + (-side(agent.team)*2000), 200)
        rightfield = Vector3(side(agent.team)*4200, agent.ball.location.y + (-side(agent.team)*2000), 200)
        targets = {'foe_goal': (agent.foe_goal.left_post, agent.foe_goal.right_post), 'away_from_our_net': (
            agent.friend_goal.right_post, agent.friend_goal.left_post), 'upfield': (leftfield, rightfield)}
        hits = find_hits(agent, targets)
        # dribble_counter_hits = find_hits(agent, targets, z_extra=300)
        closest_large_boost = agent.get_closest_large_boost(agent.foe_goal)
        ball_distance = agent.me.location.dist(agent.ball.location)
        ball_to_goal = agent.friend_goal.location.dist(agent.ball.location)
        goal_distance = home.dist(agent.ball.location)
        our_closest_to_ball = closest_car(agent.friends + [agent.me,], agent.ball.location)
        div = 1 if agent.team == 1 else -1

        # dribbler = agent.dribbler.get_dribbler(agent, 1/120)
        # valid_dribbler = True if dribbler != None and dribbler.team != agent.team and agent.dribbler.duration > 0.4 else False
        # if agent.index == 0:
        #     agent.text2d("Dribbler Found: " + str(valid_dribbler), Vector3(40, 40, 0), 2, 2)
        #     agent.text2d("Dribble Duration: " + str(agent.dribbler.duration), Vector3(40, 70, 0), 2, 2)
        #     agent.text2d("Ball-Z-Check: " + str(agent.ball.location.z > agent.dribbler.z_req), Vector3(40, 100, 0), 2, 2)
        #     agent.text2d("Dist-Check: " + str(agent.foes[0].location.dist(agent.ball.location) < agent.dribbler.dist_req), Vector3(40, 130, 0), 2, 2)
        #     agent.text2d("Car-Check: " + str(agent.foes[0].index == (agent.dribbler.prev_car.index if agent.dribbler.prev_car is not None else -1)), Vector3(40, 160, 0), 2, 2)
        #     agent.text2d("Car-Info: " + str(agent.foes[0].index) + " || " + str(agent.dribbler.prev_car.index), Vector3(40, 190, 0), 2, 2)

        nobody_back = True
        for car in agent.friends:
            if car.location.dist(agent.friend_goal.location) >= agent.me.location.dist(agent.friend_goal.location):
                nobody_back = False
        
        nobody_back = False # 1v1 placeholder
            
        if agent.intent is None:
            if agent.kickoff_flag:
                go_kickoff = True
                for car in agent.friends:
                    if car.location.dist(agent.ball.location) <= ball_distance:
                        if car.location.dist(agent.ball.location) < ball_distance:
                            go_kickoff = False
                        elif car.location.dist(agent.ball.location) == ball_distance and not (agent.me.location.x * div < 0):
                            go_kickoff = False
                        
                agent.set_intent(kickoff() if go_kickoff else goto_boost(closest_large_boost))
                return

            else:
                home_dist = home.dist(agent.me.location)
                # #if not nobody_back:
                # if ball_to_goal < 6000 and valid_dribbler:# and our_closest_to_ball.index == agent.me.index and goal_distance < 650:
                #     if len(dribble_counter_hits['upfield']) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 6500:
                #         agent.set_intent(dribble_counter_hits['upfield'][0])
                #         return
                    
                #     elif len(dribble_counter_hits['foe_goal']) > 0:
                #         agent.set_intent(dribble_counter_hits['foe_goal'][0])
                #         return

                #     elif len(dribble_counter_hits['away_from_our_net']) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 1200:
                #         agent.set_intent(dribble_counter_hits['away_from_our_net'][0])
                #         return
                    
                #     else:
                #         agent.set_intent(demo(dribbler))
                #         return 
                ball_distance_plus = (agent.ball.location + agent.ball.velocity.flatten()).dist(home)
                if (agent.me.boost >= 20 or ball_distance_plus < 2500) and not nobody_back and (agent.foe_goal.location.dist(agent.ball.location) > 5500 if abs(agent.ball.location.x) > 2500 else True):
                    if len(hits['foe_goal']) > 0 and agent.ball.location.dist(agent.foe_goal.location) < 2000:
                        agent.set_intent(hits['foe_goal'][0])
                        return

                    elif len(hits['upfield']) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 6500:
                        agent.set_intent(hits['upfield'][0])
                        return
                    
                    elif len(hits['foe_goal']) > 0:
                        agent.set_intent(hits['foe_goal'][0])
                        return

                    elif len(hits['away_from_our_net']) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 1200:
                        agent.set_intent(hits['away_from_our_net'][0])
                        return
                    
                    else:
                        if agent.me.boost < 20 and ball_distance_plus > 3200:
                            agent.set_intent(goto_boost(closest_large_boost))
                            return
                        
                        elif home_dist > 660:
                            drive_to(home)
                            return
                        
                else:
                    if agent.me.boost < 20 and ball_distance_plus > (3200 if not nobody_back else 4300):
                        agent.set_intent(goto_boost(closest_large_boost))
                        return
                    
                    elif home_dist > 660:
                        drive_to(home)
                        return
        
