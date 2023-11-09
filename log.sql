-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';

-- I was able to get closer informations
-- .schema interviews
SELECT name, transcript FROM interviews
WHERE month = 7 AND day = 28;

-- Investigating information from witness Ruth
-- .schema bakery_security_logs
SELECT minute, license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND activity = 'exit';

-- Investigating information from witness Eugene
-- .schema atm_transactions
SELECT account_number FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

.schema bank_accounts
SELECT name, atm_transactions.account_number FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7 AND atm_transactions.day = 28
AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw';

-- Investigating information from witness Raymond (call)
-- .schema phone_calls
SELECT caller, receiver FROM phone_calls
WHERE month = 7 AND day = 28 AND duration < 60;

-- .schema people
SELECT people.name, phone_calls.caller FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration < 60;

SELECT people.name, phone_calls.receiver FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration < 60;

-- Investigating information from witness Raymond (flight)
-- .schema flights
-- .schema airports
-- .schema passengers
SELECT * FROM flights
WHERE month = 7 AND day = 29 AND origin_airport_id = 8
ORDER BY hour ASC;

SELECT id, city FROM airports;

SELECT name, phone_number, license_plate, people.passport_number FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id = 36;

-- Write a name of the thief
SELECT DISTINCT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
JOIN flights ON flights.id = passengers.flight_id
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE (phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration < 60)
AND (flights.month = 7 AND flights.day = 29 AND flights.id = 36)
AND (atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw')
AND (bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 AND bakery_security_logs.hour = 10 AND bakery_security_logs.activity = 'exit')
;
