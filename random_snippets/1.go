package main

import (
	"fmt"
	"log"
	"time"

	"github.com/dgrijalva/jwt-go"
	"golang.org/x/crypto/bcrypt"
)

var jwtSecret = []byte("my_secret_key")

type User struct {
	ID       int
	Username string
	Password string
}

func hashPassword(password string) (string, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	return string(hashedPassword), err
}

func checkPassword(hashedPassword, password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	return err == nil
}

func generateToken(userID int) (string, error) {
	claims := jwt.MapClaims{
		"user_id": userID,
		"exp":     time.Now().Add(time.Hour * 24).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}

func verifyToken(tokenString string) (*jwt.Token, error) {
	return jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return jwtSecret, nil
	})
}

func main() {
	user := User{ID: 1, Username: "nurlan"}

	hashedPassword, err := hashPassword("supersecret")
	if err != nil {
		log.Fatal("Error hashing password:", err)
	}
	user.Password = hashedPassword
	fmt.Println("Hashed Password:", user.Password)

	if checkPassword(user.Password, "supersecret") {
		fmt.Println("Password is correct!")
	} else {
		fmt.Println("Invalid password!")
	}

	token, err := generateToken(user.ID)
	if err != nil {
		log.Fatal("Error generating JWT:", err)
	}
	fmt.Println("Generated JWT:", token)

	parsedToken, err := verifyToken(token)
	if err != nil {
		log.Fatal("Invalid token:", err)
	} else {
		fmt.Println("Token is valid:", parsedToken.Valid)
	}
}
