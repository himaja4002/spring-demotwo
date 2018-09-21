package com.springdemotwo;

import java.util.Random;

public class HappyFortuneService implements FortuneService {
	int j;
	Random rand = new Random();

	@Override
	public String getFortune() {
		String[] fortune = {" Today is your lucky day", "Better luck next time", "Sad fortune"};
		j = rand.nextInt(4);
		System.out.println("fortune"+ fortune[j]);
		return fortune[j];

	}

}
