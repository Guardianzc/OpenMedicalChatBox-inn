import pickle
import copy
import numpy as np
import torch

device = torch.device("cuda:3" if torch.cuda.is_available() else "cpu")
sys_inform_slots = ['disease']

start_dia_acts = {
    'request': ['disease']
}
#path = '/remote-home/czhong/RL/data/data/dataset/label/allsymptoms/dataset_dxy/'
#path = '/remote-home/czhong/RL/data/new_data/mz10/allsymptoms/dataset_dxy/'
#path = '/remote-home/czhong/RL/Dialogue-System-for-Automatic-Diagnosis-master/dataset_dxy/'
path='/remote-home/czhong/RL/data/Fudan-Medical-Dialogue2.0/synthetic_dataset//allsymptoms//dataset_dxy/'
# dxy
with open(path + 'diseases_dxy.txt','r', encoding = 'utf-8') as f:
    disease_readline = f.readlines()

with open(path + 'symptoms_dxy.txt','r', encoding = 'utf-8') as f:
    symptoms_readline = f.readlines()
sys_inform_slots_values = list()
sys_request_slots = list()
for i in disease_readline:
    sys_inform_slots_values.append(i.rstrip('\n'))
    
for i in symptoms_readline:
    sys_request_slots.append(i.rstrip('\n'))
# sys_inform_slots_values = ['小儿腹泻', '小儿手足口病', '过敏性鼻炎', '上呼吸道感染']
# sys_request_slots = ['稀便', '厌食', '精神萎靡', '尿少', '发热', '烦躁不安', '疱疹', '咽部不适', '淋巴结肿大', '鼻塞', '咳嗽', '抽动', '皮疹', '流涎', '咳痰', '喷嚏', '流涕', '绿便', '腹痛', '肠鸣音亢进', '呕吐', '盗汗', '呼吸困难', '肛门排气增加', '反胃', '蛋花样便', '腹胀', '过敏', '鼻痒', '呼吸音粗', '头痛', '鼻衄', '眼部发痒', '臭味', '舌苔发白', '口渴', '畏寒', '嗳气', '体重减轻']
sys_request_slots_highfreq = sys_request_slots[:20]



# muzhi

# sys_inform_slots_values = ['上呼吸道感染', '小儿支气管炎', '小儿腹泻', '小儿消化不良']
# sys_request_slots_highfreq = ['发热', '咳嗽', '鼻流涕', '普通感冒', '中等度热', '有痰', '鼻塞', '低热', '喷嚏', '呕吐', '支气管炎', '痰鸣音', '咳痰', '急性气管支气管炎', '腹泻', '稀便', '水样便', '消化不良', '绿便', '血便', '大便粘液', '屁', '哭闹', '厌食']
# sys_request_slots = ['普通感冒', '干咳', '咳嗽', '厌食', '发热', '上呼吸道感染', '中等度热', '出汗', '高热', '头痛', '咽喉不适', '低热', '呕吐', '精神软', '鼻流涕', '喷嚏', '鼻塞', '四肢厥冷', '急性气管支气管炎', '咳痰', '稀便', '食欲不佳', '腹痛', '恶心', '干呕', '肠炎', '过敏', '有痰', '痰鸣音', '扁桃体炎', '退热', '支气管炎', '大便酸臭', '消化不良', '腹泻', '气管炎', '肺炎', '血便', '皮疹', '咽喉炎', '喘息', '水样便', '食欲不振', '绿便', '肛门红肿', '支气管肺炎', '口臭', '哭闹', '湿疹', '鼻炎', '病毒感染', '睡眠障碍', '反复发热', '嗜睡', '便秘', '贫血', '大便粘液', '粗糙呼吸音', '腹胀', '屁', '沙哑', '细菌感染', '尿量减少', '腹部不适', '肠鸣音', '支原体感染']

#print(len(sys_request_slots))
################################################################################
# Dialog status
################################################################################
FAILED_DIALOG = -1
SUCCESS_DIALOG = 1
NO_OUTCOME_YET = 0

# Rewards
SUCCESS_REWARD = 50
FAILURE_REWARD = 0
PER_TURN_REWARD = 0


################################################################################
#  Diagnosis
################################################################################
NO_DECIDE = 0
NO_MATCH = "no match"
NO_MATCH_BY_RATE = "no match by rate"

################################################################################
#  Special Slot Values
################################################################################
I_AM_NOT_SURE = -1
I_DO_NOT_CARE = "I do not care"
NO_VALUE_MATCH = "NO VALUE MATCHES!!!"

################################################################################
#  Slot Values
################################################################################
TRUE = 1
FALSE = -1
NOT_SURE = -2
NOT_MENTION = 0

################################################################################
#  Constraint Check
################################################################################
CONSTRAINT_CHECK_FAILURE = 0
CONSTRAINT_CHECK_SUCCESS = 1

################################################################################
#  NLG Beam Search
################################################################################
nlg_beam_size = 10


################################################################################
#   A Basic Set of Feasible actions to be Consdered By an RL agent
################################################################################
feasible_actions = [

    ############################################################################
    #   thanks actions
    ############################################################################
    {'diaact':"thanks", 'inform_slots':{}, 'request_slots':{}},
    {'diaact': "inform", 'inform_slots': { 'disease': 'UNK', 'taskcomplete': "PLACEHOLDER"}, 'request_slots': {} }

]
############################################################################
#   Adding the inform actions
############################################################################
for slot_val in sys_inform_slots_values:
    slot = 'disease'
    feasible_actions.append({'diaact':'inform', 'inform_slots':{slot:slot_val, 'taskcomplete': "PLACEHOLDER"}, 'request_slots':{}})
############################################################################
#   Adding the request actions
############################################################################
for slot in sys_request_slots:
    feasible_actions.append({'diaact':'request', 'inform_slots':{}, 'request_slots': {slot: 'UNK'}})

