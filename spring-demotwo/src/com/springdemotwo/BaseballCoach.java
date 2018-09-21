package com.springdemotwo;

public class BaseballCoach implements Coach {
	
	//prvate field for dependency
	private FortuneService fortuneService;
	
	//define a constructor for dependency injection
	public BaseballCoach(FortuneService theFortuneService) {
		fortuneService = theFortuneService;
	}
	@Override
	public String getDailyWorkout() {
		return "Batting on 30 mins";
	}

	@Override
	public String getDailyFortune() {
		return fortuneService.getFortune();
	}

}
