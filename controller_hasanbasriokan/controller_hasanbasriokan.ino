#define ENCODER1 2 
#define ENCODER3 3 
#define PWM 5
#define IN1 10
#define IN2 9


volatile float GecenZaman,suan, gecmis = 0,rpm ,cikis_controller;
float kp = 40, kd = 1, ki = 0.5, hedef_deger= 100, dt = 0.01;
float integral_degiskeni =0, hata_gecmis=0, hata;
float pidDeger;

//pid yi hesapladığımız fonksiyonumuz.
void pid(float kp, float kd, float ki, float dt, float hata, float hata_gecmis) {
  integral_degiskeni = integral_degiskeni +dt* hata_gecmis;
  pidDeger = (kp*hata) + (ki*integral_degiskeni) + (kd*(hata-hata_gecmis)/dt);
}

//Encoderden veriyi burada okuyoruz. 
void EncoderVeriOkuma(){
 //Bilgisayar saatini microsaniye olarak alıyoruz.
  suan = micros();
 //Micros cinsinden şuandaki zaman ile, micros cinsinden bir önceki zamanı bularak gecen zamanıhesaplıyoruz.
  GecenZaman = suan - gecmis;
 // Rotate per minute yani bir dakikadaki dönüş sayısını hesaplıyoruz.
 //hesapları yaparken, 60 dakikadan, 1000000 microsaniyeden, 24 ise encoderin
 //saniiyede ürettiği pulse sayısından kaynaklanmaktadır.
  rpm = 60*1000000/(24*GecenZaman);
  gecmis=suan;
}

void setup() {
  Serial.begin(9600);
  pinMode(ENCODER1,INPUT);
  pinMode(ENCODER3,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCODER1),EncoderVeriOkuma,RISING);
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
 }

void loop(){
  int yon = 1;

  //Burası seri haberleşmeden kp,ki,kd ve hız değerini almak içindir.
  if (Serial.available()){
    String veri = Serial.readString();
    String sayi = veri.substring(1);
    if (veri.substring(0).equals("P"))
    {kp = veri.toInt();}
    else if (veri.substring(0).equals("I"))
    {ki = veri.toInt();}
    else if (veri.substring(0).equals("D"))
    {kd = veri.toInt();}
    else if (veri.substring(0).equals("H"))
    {hedef_deger = veri.toInt();}
   }
  //feedback controllerin çıkışını rpm değerine atıyoruz.
  cikis_controller = rpm;
    Serial.println(cikis_controller);
  //hedef değer ile rpm değerinin farkı hatayı vermektedir.
  hata= hedef_deger - cikis_controller;
  //pid fonksiyonunu çağırıyoruz.
  pid(kp,ki,kd,dt,hata,hata_gecmis);
  //hata artık geçmiş hataımız oldu. PID fonksiyonunda tekrardan kullanamk için bu şekilde yaptık.
  hata_gecmis=hata;

 // Eğer pid in değeri sıfırdan kücükse yon cw nin tersi yani ccw olacaktır. bunu -1 ile ifade ettim. 
    if(pidDeger<0)
    {yon = -1;}
    
//Motorun sağa ya da sola dönmesini sağlayan kod parçası  
  analogWrite(PWM,pidDeger);
  //Yon 1 ise motorun CW yönünde dönmesini sağlıyor
  if(yon == 1){
    digitalWrite(IN1,HIGH);
    digitalWrite(IN2,LOW);
  }
  //Yon -1 ise motorun CCW yönünde dönmesini sağlıyor
  else if(yon == -1){
    digitalWrite(IN1,LOW);
    digitalWrite(IN2,HIGH);
  }
  //Diğer durumlar anlamsız davranış olduğu için motoru durduruyor.
  else{
    digitalWrite(IN1,LOW);
    digitalWrite(IN2,LOW);
  }
}
