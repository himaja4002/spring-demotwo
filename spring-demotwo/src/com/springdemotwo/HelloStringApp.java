package com.springdemotwo;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class HelloStringApp {

	public static void main(String[] args) {
		
		//load the spring configuration file
		
		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
				// retrieve it from bean container
		
		Coach theCoach = context.getBean("myCoach",Coach.class);
		//call the method
		System.out.println(theCoach.getDailyWorkout());
		//close the container
		context.close();

	}

}
