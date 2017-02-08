Feature: Teste dos comandos IPWALL

  @delete_all_ipwalls
  Scenario: requisicao delete_all_ipwalls
    Given um comando server->cpu "delete_all_ipwalls"
    Then recebe "sucesso no ack"

  @insert_ipwall
  Scenario: requisicao insert_ipwall
    Given um comando server->cpu "insert_ipwall"
    Then recebe "sucesso no ack"
      
  @start_emergency
  Scenario: requisicao start_emergency
    Given um comando server->cpu "start_emergency"
    When recebe o ack do comando
    Then recebe resposta cpu->server "emergency_started"

  @stop_emergency
  Scenario: requisicao stop_emergency
    Given um comando server->cpu "stop_emergency"
    When recebe o ack do comando
    Then recebe resposta cpu->server "emergency_stoped"
   
  @get_relays_status
   Scenario: requisicao get_relays_status
     Given um comando server->cpu "get_relays_status ipwall_id: 3"
     When recebe o ack do comando
     Then recebe resposta cpu->server "send_relays_status"
 
  @open_the_door
  Scenario: requisicao open_the_door
    Given um comando server->cpu "open_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"
 
  @close_the_door
  Scenario: requisicao close_the_door
    Given um comando server->cpu "close_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"
 
  @keep_the_door_opened
  Scenario: requisicao keep_the_door_opened
    Given um comando server->cpu "keep_the_door_opened ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"
 
  @close_the_door
  Scenario: requisicao close_the_door
    Given um comando server->cpu "close_the_door ipwall_id: 3, door_id: 1"
    When recebe o ack do comando
    Then recebe resposta cpu->server "sensor_status_changed"
 
  @reset_ipwall
  Scenario: requisicao reset_ipwall
    Given um comando server->cpu "reset_ipwall id: 3"
    When recebe o ack do comando
    Then recebe resposta cpu->server "ipwall_started"
 
  @update_ipwall
  Scenario: requisicao update_ipwall
    Given um comando server->cpu "update_ipwall"
    When recebe o ack do comando
    Then recebe resposta cpu->server "update_ipwall_result"
 
 
