#define BRAKEVCC 0
#define PARA_FRENTE 1
#define PARADO 0
#define PARA_TRAZ -1
#define BRAKEGND 3
#define CS_THRESHOLD 15   // Definição da corrente de segurança (Consulte: "1.3) Monster Shield Exemplo").

short usSpeed = 150; 

int inApin[2] = {4, 11};// INA: Sentido Horário Motor0 e Motor1 (Consulte:"1.2) Hardware Monster Motor Shield").
int inBpin[2] = {5, 10}; // INB: Sentido Anti-Horário Motor0 e Motor1 (Consulte: "1.2) Hardware Monster Motor Shield").
int pwmpin[2] = {6, 9};            // Entrada do PWM
int cspin[2] = {1, 2};              // Entrada do Sensor de Corrente


void setup() {                     // Faz as configuração para a utilização das funções no Sketch

  Serial.begin(9600);              // Iniciar a serial para fazer o monitoramento
 
  for (int i = 0; i < 2; i++)
  {
    pinMode(inApin[i], OUTPUT);
    pinMode(inBpin[i], OUTPUT);
    pinMode(pwmpin[i], OUTPUT);
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);

  }
}

    void loop()
    {
      char user_input;

      while (Serial.available())
      {
        user_input = Serial.read(); //Read user input and trigger appropriate function
      

        if (user_input == '1')
        {
          Stop();
        }
        else if (user_input == '2')
        {
          Forward();
        }
        else if (user_input == '3')
        {
          Reverse();
        }
        else if (user_input == '+')
        {
          IncreaseSpeed();
        }
        else if (user_input == '-')
        {
          DecreaseSpeed();
        }
        else
        {
          Serial.println("Invalid option entered.");
        }

      }
    }

    void Stop()
    {
      Serial.println("Stop");
    
      motorGo(PARADO,PARADO, PARADO,PARADO);
    }

    void Forward()
    {
      Serial.println("Forward");
    
      motorGo(1,1, usSpeed, usSpeed);
    }

    void Reverse()
    {
      Serial.println("Reverse");
      
      motorGo(-1,-1 ,usSpeed, usSpeed);
    }

    void IncreaseSpeed()
    {
      usSpeed = usSpeed + 10;
      if (usSpeed > 255)
      {
        usSpeed = 255;
      }

      Serial.print("Speed +: ");
      Serial.println(usSpeed);

    }

    void DecreaseSpeed()
    {
      usSpeed = usSpeed - 10;
      if (usSpeed < 0)
      {
        usSpeed = 0;
      }

      Serial.print("Speed -: ");
      Serial.println(usSpeed);

     
    }

    void motorGo(uint8_t direct_motor1, uint8_t direct_motor2, uint8_t pwm_motor1, uint8_t pwm_motor2) { //Function that controls the variables: motor(0 ou 1), direction (cw ou ccw) e pwm (entra 0 e 255);


      if (direct_motor1 == PARA_FRENTE && direct_motor2 == PARA_FRENTE) {

        digitalWrite(inApin[0], LOW);
        digitalWrite(inBpin[0], HIGH);
        digitalWrite(inApin[1], LOW);
        digitalWrite(inBpin[1], HIGH);
      }
      else if (direct_motor1 == PARA_TRAZ && direct_motor2 == PARA_TRAZ) {

        digitalWrite(inApin[0], HIGH);
        digitalWrite(inBpin[0], LOW);
        digitalWrite(inApin[1], HIGH);
        digitalWrite(inBpin[1], LOW);

      }

      else if (direct_motor1 == PARADO && direct_motor2 == PARADO  ) {

        digitalWrite(inApin[0], LOW);
        digitalWrite(inBpin[0], LOW);
        digitalWrite(inApin[1], LOW);
        digitalWrite(inBpin[1], LOW);

      }

      analogWrite(pwmpin[0], pwm_motor1);
      analogWrite(pwmpin[1], pwm_motor2);
    }

  

}
