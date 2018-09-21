package com.springdemotwo;

public class CricketCoach implements Coach {
	private String emailAddress;
	private String team;
	
	
	
	public String getEmailAddress() {
		return emailAddress;
	}


	public void setEmailAddress(String emailAddress) {
		System.out.println("inside set email address");
		this.emailAddress = emailAddress;
	}


	public String getTeam() {
		return team;
	}


	public void setTeam(String team) {
		System.out.println("inside setter - team");
		this.team = team;
	}


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
