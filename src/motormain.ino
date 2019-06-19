#define BRAKEVCC 0
#define CW 1
#define CCW 2
#define BRAKEGND 3
#define CS_THRESHOLD 15   // Definição da corrente de segurança (Consulte: "1.3) Monster Shield Exemplo").

 

int inApin[2] = {4, 11}// INA: Sentido Horário Motor0 e Motor1 (Consulte:"1.2) Hardware Monster Motor Shield").
int inBpin[2] = {5, 10}; // INB: Sentido Anti-Horário Motor0 e Motor1 (Consulte: "1.2) Hardware Monster Motor Shield").
int pwmpin[2] = {6, 9};            // Entrada do PWM
int cspin[2] = {1, 2};              // Entrada do Sensor de Corrente

int statpin = 13;
int i=0;;
void setup()                         // Faz as configuração para a utilização das funções no Sketch
{
Serial.begin(9600);              // Iniciar a serial para fazer o monitoramento
pinMode(statpin, OUTPUT);
for (int i=0; i<2; i++)
    {
    pinMode(inApin[i], OUTPUT);
    pinMode(inBpin[i], OUTPUT);
    pinMode(pwmpin[i], OUTPUT);
    }
for (int i=0; i<2; i++)
    {
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);
    }
}

void loop()                          // Programa roda dentro do loop
{
while(i<255)
    {
    motorGo(0, CW, i);             // Aumento do o PWM do motor até 255
    delay(50);                          // Se o motor travar ele desliga o motor e
    i++;                                  // Reinicia o processo de aumento do PWM
    if (analogRead(cspin[0]) > CS_THRESHOLD)
    motorOff(0);
    Serial.println(i);
    digitalWrite(statpin, LOW);
    }
i=1;
while(i!=0)
    {                                      // Mantém o PWM em 255 (Velocidade Máxima do Motor)
    motorGo(0, CW, 255);       // Se o motor travar ele desliga o motor e
    if (analogRead(cspin[0]) > CS_THRESHOLD)              // Reinicia o processo de aumento do PWM
    motorOff(0);
    }
}
void motorOff(int motor)     //Função para desligar o motor se o mesmo travar
{

for (int i=0; i<2; i++)
    {
    digitalWrite(inApin[i], LOW);
    digitalWrite(inBpin[i], LOW);
    }
analogWrite(pwmpin[motor], 0);
i=0;
digitalWrite(13, HIGH);
Serial.println("Motor Travado");
delay(1000);
}
void motorGo(uint8_t motor, uint8_t direct, uint8_t pwm)         //Função que controla as variáveis: motor(0 ou 1), sentido (cw ou ccw) e pwm (entra 0 e 255);
{
if (motor <= 1)
    {
    if (direct <=4)
        {
        if (direct <=1)
            digitalWrite(inApin[motor], HIGH);
        else
            digitalWrite(inApin[motor], LOW);

        if ((direct==0)||(direct==2))
            digitalWrite(inBpin[motor], HIGH);
        else
            digitalWrite(inBpin[motor], LOW);

        analogWrite(pwmpin[motor], pwm);
        }
    }
}
