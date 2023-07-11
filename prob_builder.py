import copy
import distance

class Prob_Instance:
    def __init__(self):
        self.objective = 'Total_Cost'
        self.ord_list = [] # order list
        self.car_list = [] # car list

    def deepcopy(self):
        return copy.deepcopy(self)

class Order: # 입력 데이터: car (요청)
    def __init__(self, ORD_NO, arrive_latitude, arrive_longitude, arrive_ID, CBM, start_tw, end_tw, work_time,
                 terminal_ID, date, Group, start_latitude, start_longitude):
        self.ord_no = ORD_NO    # 주문 ID
        self.final_coord = [arrive_latitude,arrive_longitude]   # 도착지 좌표
        self.arrive_id = arrive_ID  # 도착지 ID
        self.cbm = CBM  # 상품 CBM
        self.time_window = [start_tw, end_tw]   # 하차 가능시간
        self.work_time = work_time      # 하차 작업시간
        self.terminal_ID = terminal_ID  # 터미널ID (출발지)
        self.start_coord = [start_latitude, start_longitude] # 터미널 좌표
        self.date = date    # 주물 발생 날짜
        self.group = Group  # 그룹

        self.vehicle_id = None  # 할당된 차량 ID
        self.sequence = None      # 할당된 배송 시퀀스
        self.site_code = None   # 도착지 ID
        self.arrival_time = None    # 도착시각
        self.waiting_time = None    # 대기시간
        self.service_time = None    # 상하/하차시간
        self.departure_time = None  # 출발시각
        self.delivered = None       # 배송 완료 여부
        self.done = False

    def initialize(self):
        self.done = False

    def __repr__(self):
        return str(self.ord_no)

class Car: # 이동 차량
    def __init__(self, VehicleID, max_capa, start_center,fixed_cost, variable_cost, latitude, longitude):
        self.vehicle_id = VehicleID
        self.start_center = start_center
        self.coord = [latitude,longitude]
        self.conut = 0
        self.volume = 0     # 현재 적재량
        self.total_volume = 0   # 누적 적재량
        self.travel_distance = 0    # 총 주행거리
        self.work_time = 0      # 총 작업 시간
        self.travel_time = 0    # 총 이동 시간
        self.service_time = 0   # 총 하역 시간
        self.waiting_time = 0   # 총 대기 시간
        self.total_fixed_cost = 0   # 누적된 차량 고정비
        self.total_variable_cost = 0    # 누적된 차량 변동비
        self.max_capa = max_capa    # 적재 capa_max
        self.fixed_cost = fixed_cost    # 차량 고정비
        self.variable_cost = variable_cost  # 차량 변동비


    def initialize(self):
        self.served_order = []
        self.can_move = True

    def loading(self, target: Order):
        if not self.doable(target): raise Exception('Infeasible Loading!')
        target.done = True
        dist, time = distance.calculate_distance_time(self.start_center, target.terminal_ID)
        self.travel_distance += dist
        self.travel_time += time
        self.volume += target.cbm
        self.total_volume += target.cbm
        self.conut += 1
        self.coord = target.start_coord

    def doable(self, target: Order) -> bool: # -> return 값 힌트
        if target.done:
            return False
        elif self.max_capa < self.volume + target.cbm:
            return False
        else:
            return True

    def __repr__(self):
        return str(self.vehicle_id)