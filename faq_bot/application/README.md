# Application Layer (애플리케이션 계층)

애플리케이션의 서비스 인터페이스를 다루는 계층입니다. 사용자 요청을 받아서 도메인 로직을 실행하고 결과를 반환합니다. FastAPI의 엔드포인트가 여기에 속합니다.
---
- ChatService 클래스는 외부 요청(여기서는 FastAPI로 들어오는 API 요청)을 처리하는 역할을 하며, 도메인 계층과 인프라 계층의 기능을 적절히 호출합니다.
- 이 계층은 주로 비즈니스 로직을 수행하지 않고, 도메인 계층을 호출하여 실제 비즈니스 로직을 실행하고, 그 결과를 외부에 반환하는 역할을 합니다. 이는 헥사고날 아키텍처에서 중요한 중재자 역할을 합니다.