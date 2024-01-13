import http from "k6/http";
import { check } from "k6";

export const options = {
  stages: [
    { target: 200, duration: "30s" },
    { target: 0, duration: "30s" },
  ],
};

export default function () {
  const result = http.get("http://polymetrie-increment-service:5000/metrics");
  check(result, {
    "http response status code is 200": result.status === 200,
  });

  const postResult = http.post(
    "http://polymetrie-increment-service:5000/api/clients"
  );
  check(postResult, {
    "http response status code is 201": postResult.status === 201,
  });

  const postResult2 = http.post(
    "http://polymetrie-increment-service:5000/api/visits"
  );
  check(postResult2, {
    "http response status code is 201": postResult2.status === 201,
  });

  const getResult = http.get(
    "http://polymetrie-increment-service:5000/api/fetch-db"
  );
  check(getResult, {
    "http response status code is 200": getResult.status === 200,
  });

  const getResult2 = http.get(
    "http://polymetrie-increment-service:5000/api/fetch-redis"
  );
  check(getResult2, {
    "http response status code is 200": getResult2.status === 200,
  });
}
