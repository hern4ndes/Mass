
#define BRAKEVCC 0
#define PARA_FRENTE 1
#define PARADO 0
#define PARA_TRAZ 2
#define BRAKEGND 3
#define CS_THRESHOLD 15   //não usado  

int pwmesquerda = 255;
int pwmdireita = 152;

int inApin[2] = {4, 12};            // INA: Sentido Horário Motor0 e Motor1 (Consulte:"1.2) Hardware Monster Motor Shield").
int inBpin[2] = {5, 11};            // INB: Sentido Anti-Horário Motor0 e Motor1 (Consulte: "1.2) Hardware Monster Motor Shield").
int pwmpin[2] = {6, 10};            // Entrada do PWM
int cspin[2] = {1, 2};              // Entrada do Sensor de Corrente

void setup() {                      // Faz as configuração para a utilização das funções no Sketch



  for (int i = 0; i < 2; i++)
  {
    pinMode(inApin[i], OUTPUT);
    pinMode(inBpin[i], OUTPUT);
    pinMode(pwmpin[i], OUTPUT);
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);

  }
  Serial.begin(115200);             // Iniciar a serial para fazer o monitoramento

  while (!Serial) {
    ;                               //não faz nada até que a coominicação seja iniciada
  }

}

void loop() {
  
  int pwm_left = 0;
  int pwm_right = 0;

  if (Serial.available() > 0) {
    
    pwm_left = Serial.readStringUntil(':').toInt();
    pwm_right = Serial.readStringUntil(';').toInt();

    motor_go(pwm_left, pwm_right);
    
  }

}

void reverse() {

  digitalWrite(inApin[0], HIGH);
  digitalWrite(inBpin[0], LOW);
  digitalWrite(inApin[1], HIGH);
  digitalWrite(inBpin[1], LOW);
  //  Serial.println("reverse");

}

void left() {

  digitalWrite(inApin[0], HIGH);
  digitalWrite(inBpin[0], LOW);
  digitalWrite(inApin[1], LOW);
  digitalWrite(inBpin[1], HIGH);
  //  Serial.println("left");

}
void right() {

  digitalWrite(inApin[0], LOW);
  digitalWrite(inBpin[0], HIGH);
  digitalWrite(inApin[1], HIGH);
  digitalWrite(inBpin[1], LOW);
  //  Serial.println("right");/

}

void foward() {

  digitalWrite(inApin[0], LOW);
  digitalWrite(inBpin[0], HIGH);
  digitalWrite(inApin[1], LOW);
  digitalWrite(inBpin[1], HIGH);
  //  Serial.println("foward");

}
void write_pwm(int pwm_left, int pwm_right) {
  //
  //  Serial.print(pwm_left);
  //  Serial.print("   ");
  //  Serial.println(pwm_right);
  analogWrite(pwmpin[0], abs(pwm_left));
  analogWrite(pwmpin[1], abs(pwm_right));
  //  Serial.println("updating pwm");
  //  Serial.print("pwm_left = " + pwm_left);
  //  Serial.print("pwm_righ = " + pwm_right);/

}

void motor_go(int pwm_left, int pwm_right) {
  //  Serial.print("pwm_left = >>> " + pwm_left);/
  //  Serial.print("pwm_righ = " + pwm_right); // mo/tor 2 é o da direitaFunction that controls the variables: motor(0 ou 1), direction (cw ou ccw) e pwm (entra 0 e 255);
  if ((pwm_left < 0) && (pwm_right < 0)) {

    reverse();
  }

  else if ((pwm_left < 0) && (pwm_right > 0)) {

    left();

  }

  else if ((pwm_left > 0) && (pwm_right < 0)) {

    right();

  }

  else {
    foward();
  }

  write_pwm(pwm_left, pwm_right);

}
