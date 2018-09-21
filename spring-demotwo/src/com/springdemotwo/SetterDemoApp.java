package com.springdemotwo;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SetterDemoApp {
	
	public static void main(String[] args) {
		
		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
		CricketCoach theCoach = context.getBean("myCricketCoach",CricketCoach.class);
		//call method
		System.out.println(theCoach.getDailyWorkout());
		System.out.println(theCoach.getDailyFortune());
		context.close();
	}

}
