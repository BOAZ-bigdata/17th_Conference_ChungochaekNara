<h4 align="center"> 실시간 데이터를 이용한 </h4>

<h1 align="center"> Elasticsearch 인덱싱 성능 최적화 </h1>

## Introduction

실시간 데이터를 이용한 Elastic 인덱싱 성능 최적화 실험 및 결과 보고

## Data
알라딘 API 데이터 스키마 이용
필드가 더 많이 중첩되어있는 상황을 가정하여 nested field 추가

## Environment

![image](https://user-images.githubusercontent.com/66217855/214418669-6897ed7b-ed42-430f-a866-92e980fa50fc.png)

## Architecture

![architecture](https://user-images.githubusercontent.com/66217855/215096293-f45ef27c-5c3f-4446-901c-fe4cb78eaa75.png)

## Indexing Optimization

`IR` Indexing Rate  
`IL` Indexing Latency  

### Dynamic Mapping vs Static Mapping

<table>
  <tr>
    <td>분류</td>
    <td>Dynamic</td>
    <td>Static</td>
  </tr>
  <tr>
    <td rowspan="2">IR</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214422131-64e00e3b-c9cf-4654-8311-4a1befca8dfb.png" width="200">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214426050-6015e866-b094-4dd9-b3b4-be354b445779.png" width="200">
  </tr>
  <tr>
    <td>604.83 /s</td>
    <td>638.24 /s</td>
  </tr>
  <tr>
    <td rowspan="2">IL</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214422656-b937f438-08bd-4b02-b10b-63620d673e3f.png" width="200">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214426197-e7cfa301-3884-49c7-92d4-adb73ec5b054.png" width="200">
  </tr>
  <tr>
    <td>0.3ms</td>
    <td>0.17ms</td>
  </tr>
</table>

- **Static Mapping** 일 때 **최대 성능**
- 성능 향상
  - _IR 약 1.06배 증가_  
  - _IL 약 1.78배 감소_  


### Number of Primary Shards

<table>
  <tr>
    <td>분류</td>
    <td>2 shards</td>
    <td>4 shards</td>
    <td>8 shards</td>
    <td>16 shards</td>
  </tr>
  <tr>
    <td rowspan="2">IR</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427291-95ecc72f-3ebf-492f-acc3-efe9d8023b42.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427413-845805cc-9fe8-4cf4-bbf7-8513a5a110b2.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427477-adaddb1e-84d2-4476-83a1-9f2a6a9798c3.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427504-95a17ec7-d89c-41da-8a72-3bea2900e6a5.png" width="100">
  </tr>
  <tr>
    <td>653.18 /s</td>
    <td>640.79 /s</td>
    <td>647.39 /s</td>
    <td>640.91 /s</td>
  </tr>
  <tr>
    <td rowspan="2">IL</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427334-b78f72e7-f227-480b-97bd-0c9c9c10d5e1.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427551-c9182ab0-a3b4-456b-a456-ea964483e882.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427609-3ef0a4cc-a488-405b-96f6-e8cd179e5b0f.png" width="100">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427660-dfdd862b-9075-42dd-aa39-babd025b7115.png" width="100">
  </tr>
  <tr>
    <td>0.20ms</td>
    <td>0.23ms</td>
    <td>0.34ms</td>
    <td>0.44ms</td>
  </tr>
</table>

- **2 Primary shards** 일 때 **최대 성능**
- 성능 향상
  - _IR 약 1.02배 증가_  
  - _IL 약 1.60배 감소_  


### Number of Data nodes

<table>
  <tr>
    <td>분류</td>
    <td>2 nodes</td>
    <td>3 nodes</td>
    <td>4 nodes</td>
  </tr>
  <tr>
    <td rowspan="2">IR</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427291-95ecc72f-3ebf-492f-acc3-efe9d8023b42.png" width="130">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214428950-d6d70020-3ef4-41ad-a98b-4b0b2461786c.png" width="130">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214428980-a63bf612-0cbb-4a8e-a1f4-f6aecf0e9852.png" width="130">
  </tr>
  <tr>
    <td>653.18 /s</td>
    <td>590.86 /s</td>
    <td>554.23 /s</td>
  </tr>
  <tr>
    <td rowspan="2">IL</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427334-b78f72e7-f227-480b-97bd-0c9c9c10d5e1.png" width="130">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214429023-3d8d9630-25c6-4f0c-980a-13d73fd65bad.png" width="130">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214429057-c3decda2-14e9-418e-964e-76156a730bdd.png" width="130">
  </tr>
  <tr>
    <td>0.20ms</td>
    <td>0.26ms</td>
    <td>0.32ms</td>
  </tr>
</table>

- **2 Data nodes** 일 때와 성능 변화 X


### Nested field vs Unnested field

<table>
  <tr>
    <td>분류</td>
    <td>Nested</td>
    <td>Unnested</td>
  </tr>
  <tr>
    <td rowspan="2">IR</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427291-95ecc72f-3ebf-492f-acc3-efe9d8023b42.png" width="200">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214429677-a6e744ce-6c9d-4b84-9420-5d5173eb0b8d.png" width="200">
  </tr>
  <tr>
    <td>653.18 /s</td>
    <td>1983.51 /s</td>
  </tr>
  <tr>
    <td rowspan="2">IL</td>
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214427334-b78f72e7-f227-480b-97bd-0c9c9c10d5e1.png" width="200">
    <td align="center"><img src="https://user-images.githubusercontent.com/66217855/214429737-144a80f6-d41c-4c1e-91f4-0872fb3b62c1.png" width="200">
  </tr>
  <tr>
    <td>0.20ms</td>
    <td>0.07ms</td>
  </tr>
</table>

- **Unnested field** 일 때 **최대 성능**
- 성능 향상
  - _IR 약 3.04배 증가_  
  - _IL 약 2.86배 감소_  

## Conclusion

### 성능 변화

|Before Optimization|After Optimization |
|-------------------|-------------------|
|1 Ingest node      |1 Ingest node      |
|1 Master(Data) node|1 Master(Data) node|
|0 Data-only node   |1 Data-only node   |
|1 Primary shard    |2 Primary shard    |
|1 Replica shard    |1 Replica shard    |
|Dynamic mapping    |Static mapping     |
|IR: 604.83 /s      |IR: 1983.51 /s     |
|IL: 0.32 ms        |IL: 0.07 ms        |

### 한계
- PC가 한 대여서 구성의 이점 누리기 어려움
- SSD를 이용하기 때문에 GC로 인한 성능 편차 존재
- 실험의 용이성을 위해 데이터 스트림을 일정하게 하여 실제 환경과 거리감 존재
- 검생 성능 고려 X
