/*
  Système de verrouillage par code avec communication I2C
  Ce programme gère un système de verrouillage à 6 boutons, avec validation par capteur infrarouge.
  La séquence correcte est envoyée à un esclave via I2C pour déclencher l'ouverture.
  En cas d'erreur, le nombre de tentatives incorrectes est communiqué à l'esclave.

  Fonctionnement :
  - Un capteur infrarouge active la saisie du code.
  - L'utilisateur doit presser 6 boutons dans le bon ordre.
  - Si la séquence est correcte, un code de succès (10) est envoyé à l'esclave.
  - En cas d'erreur, le nombre d'erreurs (1 à 3) est envoyé à l'esclave.
  - Après 3 erreurs, le système se réinitialise après un délai.

  Créé le 19/09/2025 par [ton nom]

  Basé sur les bibliothèques Arduino et Wire.h
*/
// =============================================
// INCLUSIONS ET DÉCLARATIONS GLOBALES
// =============================================
#include <Wire.h> // Bibliothèque pour la communication I2C

int buttons_pins[6] = {2, 3, 4, 5, 6, 7}; // Broches des 6 boutons
int correct[6] = {0, 1, 2, 3, 4, 5};     // Séquence correcte à entrer
int attempts[6];                         // Tableau pour stocker les tentatives
int attemptIndex = 0;                    // Index de la tentative en cours
int error = 0;                           // Compteur d'erreurs
const int irPin = 14;                    // Broche du capteur infrarouge
int irValue = 0;                         // Valeur lue par le capteur IR

// =============================================
// FONCTION : Réinitialisation des tentatives
// =============================================
void reset_attempts() {
  attemptIndex = 0; // Remet l'index à zéro
  for (int i = 0; i < 6; i++) attempts[i] = -1; // Réinitialise le tableau des tentatives
}

// =============================================
// FONCTION : Réinitialisation complète
// =============================================
void reset_all() {
  reset_attempts(); // Réinitialise les tentatives
  error = 0;        // Remet le compteur d'erreurs à zéro
  Serial.println("Full reset");
}

// =============================================
// FONCTION : Envoi d'un code à l'esclave via I2C
// =============================================
void sendtoSlave(int code) {
  Wire.beginTransmission(8); // Adresse I2C de l'esclave
  Wire.write(code);           // Envoie le code (10 pour succès, 1-3 pour erreurs)
  Wire.endTransmission();    // Termine la transmission
  delay(50);                  // Délai pour stabiliser l'envoi
}

// =============================================
// FONCTION : Détection d'appui sur un bouton (avec anti-rebond)
// =============================================
int listenPressButton(int button) {
  if (!digitalRead(button)) { // Si le bouton est pressé (logique inversée à cause du pull-up)
    delay(20);                // Anti-rebond
    while (!digitalRead(button)) {} // Attend le relâchement du bouton
    return 1;                 // Retourne 1 si le bouton a été pressé
  }
  return 0; // Retourne 0 sinon
}

// =============================================
// CONFIGURATION INITIALE (setup)
// =============================================
void setup() {
  Wire.begin(); // Initialise la communication I2C en mode maître
  // Configure les broches des boutons en entrée avec résistance de pull-up
  for (int i = 0; i < 6; i++) pinMode(buttons_pins[i], INPUT_PULLUP);
  Serial.begin(9600); // Initialise le moniteur série
  Serial.println("Emetteur prêt");
  pinMode(irPin, INPUT); // Configure la broche du capteur IR en entrée
}

// =============================================
// BOUCLE PRINCIPALE (loop)
// =============================================
void loop() {
  // --- LECTURE DU CAPTEUR INFRAROUGE ---
  irValue = digitalRead(irPin); // Lit l'état du capteur IR

  // --- SI LE CAPTEUR DÉTECTE UN OBJET (irValue == 0) ---
  if (irValue == 0) {
    // --- DÉTECTION DES APPUIS SUR LES BOUTONS ---
    for (int i = 0; i < 6; i++) {
      if (listenPressButton(buttons_pins[i]) && attemptIndex < 6) {
        attempts[attemptIndex] = i; // Stocke l'indice du bouton pressé
        Serial.print("Button pressé: ");
        Serial.println(i + 1); // Affiche le numéro du bouton
        attemptIndex++; // Passe à la tentative suivante
      }
    }

    // --- VÉRIFICATION DE LA SÉQUENCE SI 6 BOUTONS ONT ÉTÉ PRESSÉS ---
    if (attemptIndex == 6) {
      bool correctSeq = true;
      // Compare chaque tentative avec la séquence correcte
      for (int i = 0; i < 6; i++) {
        if (attempts[i] != correct[i]) {
          correctSeq = false;
          break;
        }
      }

      // --- SÉQUENCE CORRECTE ---
      if (correctSeq) {
        Serial.println("OPEN !");
        sendtoSlave(10); // Envoie le code de succès à l'esclave
      }
      // --- SÉQUENCE INCORRECTE ---
      else {
        error++; // Incrémente le compteur d'erreurs
        if (error > 3) error = 3; // Limite le compteur à 3
        Serial.print("Erreur détectée, compteur = ");
        Serial.println(error);
        sendtoSlave(error); // Envoie le nombre d'erreurs à l'esclave

        // --- GESTION DES 3 ERREURS ---
        if (error == 3) {
          delay(7000); // Attend que l'esclave gère l'erreur (ex: clignotement)
          reset_all(); // Réinitialise tout après 3 erreurs
        }
      }
      reset_attempts(); // Réinitialise les tentatives pour une nouvelle saisie
    }
  }
  // --- SI AUCUN OBJET N'EST DÉTECTÉ PAR LE CAPTEUR IR ---
  else {
    Serial.println("Pas de valeur détectée");
    delay(500); // Délai pour éviter de saturer le moniteur série
  }
  delay(200); // Délai entre chaque itération de la boucle
}