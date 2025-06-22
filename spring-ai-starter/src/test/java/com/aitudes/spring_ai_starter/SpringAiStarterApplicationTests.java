package com.aitudes.spring_ai_starter;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;

@Import(TestcontainersConfiguration.class)
@SpringBootTest
class SpringAiStarterApplicationTests {

	@Test
	void contextLoads() {
	}

}
