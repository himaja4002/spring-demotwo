package com.springdemotwo;

public class CricketCoach implements Coach {
	
	// create no arg constructor
	public CricketCoach() {
		System.out.println("inside no-arg constructor");
	}

		
	public void setFortuneservice(FortuneService fortuneservice) {
		System.out.println("inside setter method");
		this.fortuneservice = fortuneservice;
			}


	private FortuneService fortuneservice;
	@Override
	public String getDailyWorkout() {
		return "fast bowling for 15 mins";
	}

	@Override
	public String getDailyFortune() {
		return fortuneservice.getFortune();
	}

}
