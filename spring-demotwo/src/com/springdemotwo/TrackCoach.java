package com.springdemotwo;

public class TrackCoach implements Coach {
	private FortuneService fortuneService;
	
	public TrackCoach() {
		}
	
	
	public TrackCoach(FortuneService fortuneService) {
		this.fortuneService = fortuneService;
	}

	@Override
	public String getDailyWorkout() {
		return "run 5k";
	}

	@Override
	public String getDailyFortune() {
		return "Just do it" + fortuneService.getFortune();
	}
	//add init method
	public void myStartup() {
		System.out.println("init method");
	}
	
	// add destroy
	public void myCleanup() {
		System.out.println("destroy method");
	}

}
