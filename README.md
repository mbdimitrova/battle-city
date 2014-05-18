battle-city
===========

A remake of the classic video game [Battle City](https://en.wikipedia.org/wiki/Battle_City_%28video_game%29) for the Python course at FMI.

Gameplay
--------
The player, controlling a tank, must kill the enemy tanks and protect the base from them. A level is completed when the player destroys all 20 enemy tanks. The game ends if the player loosed all available lives or the player's base is destroyed.

Obstacles
---------
There are 5 different types of obstacles on the field:
    * _Brick walls_ - can be destroyed when the player or an enemy tank shoots at them
    * _Steel walls_ - can be destroyed only when the player has collected 3 or more power up stars
    * _Bushes_ - the tanks can hide under them
    * _Water pools_ - cannot be crossed by thanks
    * _Ice fields_ - make it difficult for the player to control the tank

Power-ups
-------
Randomly appearing on the field for a period of time
    * _Tank_ - extra life
    * _Star_ - improves player's tank
    * _Bomb_ - destroys all visible enemy tanks
    * _Clock_ - feeezes all enemy tanks for a period of time
    * _Shovel_ - adds steel walls around the base for a period of time
    * _Shield_ - makes player's tank invulnerable for a period of time

Controls
--------
The player's tank is be controlled by:
* _Keyboard_
    * Move - up / down / left / right arrow keys
    * Shoot - spacebar

Highscores
----------
The highest 10 game scores are recorded


__Milestone 2:__
Смятам да реализирам основната логика за движение и стрелба на танка на играча, както и препядствията на полето. Също така ще добавя графичен интерфейс за тях.
