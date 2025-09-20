/*
  Module esclave I2C pour système de coffre-fort.
  Ce programme gère les retours visuels et sonores d'un système de coffre-fort.
  Il reçoit des codes I2C du maître et déclenche des séquences de LEDs et buzzers :
  - Code 10 : Succès (LED verte + séquence sonore de victoire)
  - Code 1 : Première erreur (LED erreur 1 + bip court)
  - Code 2 : Deuxième erreur (LED erreur 2 + bip court)
  - Code 3 : Troisième erreur (LED erreur 3 + séquence d'alarme + LED rouge clignotante)

  Brochage :
  - LEDs : 5(bleu), 7(vert), 8(rouge), 10/11/13(erreurs 1/2/3)
  - Buzzers : 14 et 15

  Fonctionnement :
  - Attend les codes I2C à l'adresse 8
  - Pour chaque code reçu, déclenche une séquence spécifique
  - Réinitialise les LEDs après traitement du code 3


  Créé le 19/09/2025 par Timeo, Joachim et Camille
  
  Basé sur les bibliothèques Arduino et Wire.h
*/

#include <Wire.h>

// Broches des composants
int buzzerPin  = 14;
int buzzerPin2 = 15;
// Variable pour stocker le code reçu
volatile int lastCode = -1;

// =============================================
// FONCTION : Déclenche un buzzer pour une durée donnée
// =============================================
void trigger_buzzer(int buzzer_pin, int delay_ms) {
  digitalWrite(buzzer_pin, HIGH);
  delay(delay_ms);
  digitalWrite(buzzer_pin, LOW);
}

// =============================================
// FONCTION : Déclenche une LED pour une durée donnée
// =============================================
void trigger_led(int led_pin, int delay_ms) {
  digitalWrite(led_pin, HIGH);
  delay(delay_ms);
  digitalWrite(led_pin, LOW);
}


// =============================================
// FONCTION : Réinitialise toutes les LEDs
// =============================================
void resetAll() {
  for (int pin = 5; pin <= 13; pin++) digitalWrite(pin, LOW);
}

// =============================================
// FONCTION : Gestion de la réception I2C
// =============================================
void receiveEvent(int howMany) {
  while (Wire.available()) {
    lastCode = Wire.read(); // Stocke le code reçu
    Serial.print("Code reçu: "); Serial.println(lastCode);
  }
}

// =============================================
// CONFIGURATION INITIALE (setup)
// =============================================
void setup() {
  Wire.begin(8);                // Initialise en esclave à l'adresse 8
  Wire.onReceive(receiveEvent); // Définit la fonction de réception

  // Configuration des broches des LEDs en sortie
  pinMode(5, OUTPUT);  // LED bleue
  pinMode(7, OUTPUT);  // LED verte
  pinMode(8, OUTPUT);  // LED rouge
  pinMode(10, OUTPUT); // LED erreur 1
  pinMode(11, OUTPUT); // LED erreur 2
  pinMode(13, OUTPUT); // LED erreur 3

  // Configuration des broches des buzzers en sortie
  pinMode(buzzerPin, OUTPUT);
  pinMode(buzzerPin2, OUTPUT);

  resetAll(); // Éteint toutes les LEDs au démarrage
  Serial.begin(9600);
  Serial.println("Esclave prêt");
}

// =============================================
// BOUCLE PRINCIPALE (loop)
// =============================================
void loop() {
  if (lastCode != -1) {
    int code = lastCode; // Copie locale du code
    lastCode = -1;       // Réinitialise le code reçu

    switch (code) {
      // --- SUCCÈS (code 10) ---
      case 10:
        digitalWrite(7, HIGH); // Allume LED verte
        // Séquence sonore de victoire
        trigger_buzzer(buzzerPin, 200);
        delay(100);
        trigger_buzzer(buzzerPin2, 300);
        delay(100);
        // Double bip rapide
        for (int i = 0; i < 2; i++) {
          digitalWrite(buzzerPin, HIGH);
          digitalWrite(buzzerPin2, HIGH);
          delay(150);
          digitalWrite(buzzerPin, LOW);
          digitalWrite(buzzerPin2, LOW);
          delay(100);
        }
        // Long bip final
        digitalWrite(buzzerPin, HIGH);
        digitalWrite(buzzerPin2, HIGH);
        delay(500);
        digitalWrite(buzzerPin, LOW);
        digitalWrite(buzzerPin2, LOW);
        delay(1000);
        resetAll();
        break;

      // --- ERREUR 1 (code 1) ---
      case 1:
        digitalWrite(10, HIGH); // Allume LED erreur 1
        trigger_buzzer(buzzerPin2, 250);
        break;

      // --- ERREUR 2 (code 2) ---
      case 2:
        digitalWrite(11, HIGH); // Allume LED erreur 2
        trigger_buzzer(buzzerPin, 250);
        break;

      // --- ERREUR 3 (code 3) ---
      case 3:
        digitalWrite(13, HIGH); // Allume LED erreur 3
        // Séquence d'alarme
        trigger_buzzer(buzzerPin, 100);
        delay(100);
        trigger_buzzer(buzzerPin2, 100);
        delay(100);
        trigger_buzzer(buzzerPin, 100);
        delay(100);
        trigger_buzzer(buzzerPin2, 100);
        delay(200);
        // LED rouge clignotante
        for (int i = 0; i < 3; i++) {
          trigger_led(8, 300);
          delay(300);
        }
        trigger_led(8, 3000); // LED rouge allumée 3 secondes
        resetAll(); // Réinitialise tout
        break;

      // --- CODE INCONNU ---
      default:
        Serial.println("Code inconnu reçu");
        break;
    }
  }
}