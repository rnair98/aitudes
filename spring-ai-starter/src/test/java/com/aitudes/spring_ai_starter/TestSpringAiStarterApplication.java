package com.aitudes.spring_ai_starter;

import org.springframework.boot.SpringApplication;

public class TestSpringAiStarterApplication {

	public static void main(String[] args) {
		SpringApplication.from(SpringAiStarterApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}
