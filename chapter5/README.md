# 📕 5장 프롬프트 프로그래밍 실전 예

5장의 보충 설명 및 소개한 프로그램 실전 예로 생성된 샘플 코드를 개제합니다.

코드 블록 오른쪽 아래 아이콘을 클릭해 코드를 복사할 수 있습니다.

- [프롬프트](PROMPT.md)를 참조하십시오.

## 5.1 시스템 정보 표시 명령어

<kbd>bash</kbd>
```
echo "=== 메모리 사용량 ===" && top -l 1 | grep PhysMem && echo -e "\n=== 드라이브 용량 ===" && df -h && echo -e "\n=== IP 주소 ===" && ifconfig | grep "inet " | grep -v 127.0.0.1
```

## 5.2 이미지 크기를 한 번에 변경해 다른 폴더에 저장하기

<kbd>bash</kbd>
```
for file in *.png; do convert "$file" -resize 50% "resized/$file"; done
```

- 샘플 데이터는 [🔗여기](sampledata/5.2_5.3/README.md)를 참조해 주십시오.

## 5.3 이미지 형식 일괄 변환 및 파일명 변경해서 저장하기

<kbd>bash</kbd>
```
mkdir -p converted && for file in *.png; do convert "$file" "converted/${file%.png}.jpg"; done
```

## 5.4 PDF 파일 결합하기

<kbd>bash</kbd>
```
for prefix in alphabet number symbol; do
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile="${prefix}_converted.pdf" "${prefix}_"*.pdf
done
```

- 샘플 데이터는 [🔗여기](sampledata/5.4/README.md)를 참조해 주십시오.


## 5.5 텍스트 파일 결합하기

<kbd>bash</kbd>
```
cat a.txt b.txt c.txt > merged.txt
```

- 샘플 데이터는 [🔗여기](sampledata/5.5/README.md)를 참조해 주십시오.

## 5.6 로그 파일에서 에러 행 추출 및 저장하기

<kbd>bash</kbd>
```
grep "ERROR:" app.log > errors.log
```

- 샘플 데이터는 [🔗여기](sampledata/5.6/README.md)를 참조해 주십시오.

## 5.7 CSV 파일 데이터 검증하기

<kbd>bash</kbd>
```
awk -F, '
NR==1 {
  cols = NF
}
NR > 1 {
    if (NF != cols)
        printf "Error: Row %d has %d columns, expected %d\n", NR, NF, cols;
    if ($1 == "" || $3 == "" || $5 == "")
        printf "Error: Row %d has empty required column(s)\n", NR;
    if ($2 !~ /^[0-9]+$/)
        printf "Error: Row %d, Column 2: Invalid integer %s\n", NR, $2;
    if ($4 !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/)
        printf "Error: Row %d, Column 4: Invalid date format %s\n", NR, $4;
    if ($6 ~ /^0/)
        printf "Warning: Row %d, Column 6: Leading zero detected %s\n", NR, $6;
}
' data.csv
```

- 샘플 데이터는 [🔗여기](sampledata/5.7/README.md)를 참조해 주십시오.

## 5.8 대량 파일의 문자 인코딩 일괄 변환하기

<kbd>bash</kbd>
```
find . -type f -name “*.txt” -exec sh -c ‘mkdir -p SJIS; nkf -s -Lw “$1” > “/tmp/${1##*/}”; mv “/tmp/${1##*/}” “SJIS/${1##*/}”’ _ {} \;
```

- 샘플 데이터는 [🔗여기](sampledata/5.8/README.md)를 참조해 주십시오.

## 5.9 생성한 명령어를 셸 스크립트로 바꾸기

<kbd>bash</kbd>
```
echo -e ‘#!/bin/bash\nmkdir -p converted\nfor file in *.png; do\n convert “$file” “converted/${file%.png}.jpg”\ndone’ > convert_images.sh && chmod +x convert_images.sh
```

<kbd>bash</kbd>
```
ls -l convert_images.sh
```

<kbd>bash</kbd>
```
./convert_images.sh
```

## 5.10 정규 표현으로 날짜 형식 통일하기

```py
import pandas as pd
from datetime import datetime
import re


# 단기 연도를 서기로 변환하는 함수
def convert_dangi_to_gregorian(dangi_date):
    # 연도를 추출하고 변환
    year = int(re.search(r’\d+’, dangi_date).group())
    gregorian_year = year - 2333

    # 원래 문자열의 연도를 대체
    return dangi_date.replace(str(year), str(gregorian_year))


# 날짜를 파싱하고 표준화하는 함수
def parse_date(date_str):
    # 단기 날짜 처리
    if ‘단기’ in date_str:
        date_str = convert_dangi_to_gregorian(date_str)

    # 가능한 날짜 형식 정의
    date_formats = [
        “%Y/%m/%d”, “%Y/%m/%d”, “%d-%m-%Y”, “%d.%m.%Y”, “%B %d, %Y”,
        “%Y년 %m월 %d일”
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime(‘%Y-%m-%d’)
        except ValueError:
            continue
    raise ValueError(f”인식할 수 없는 날짜 형식: {date_str}”)

# CSV 파일 읽기
df = pd.read_csv(‘dates.csv’)

# 날짜 파싱 함수 적용
df[‘날짜’] = df[‘날짜’].apply(parse_date)

# 업데이트된 CSV 저장
df.to_csv(‘dates_standardized.csv’, index=False)
```

```py
import pandas as pd
from datetime import datetime

# CSV 파일 읽기
df = pd.read_csv(‘dates.csv’)

# 날짜 형식 변환 함수
def convert_date(date_str):

# 단기 연도 처리
    if “단기” in date_str:
        date_str = date_str.replace(“단기 “, “”)
        year, rest = date_str.split(“년 “, 1)
        year = int(year) - 2333 # 단기를 서기로 변환
        date_str = f”{year}년 {rest}”

    # 다양한 날짜 형식을 시도
    for fmt in (“%Y/%m/%d”, “%Y-%m-%d”, “%d-%m-%Y”, “%d.%m.%Y”, “%B %d, %Y”, “%Y년 %m월 %d일”):
        try:
            return datetime.strptime(date_str, fmt).strftime(“%Y-%m-%d”)
        except ValueError:
            continue
        raise ValueError(f”날짜 형식을 변환할 수 없습니다: {date_str}”)

# 날짜 형식 변환 적용
df[‘날짜’] = df[‘날짜’].apply(convert_date)

# 변환된 CSV 파일 저장
df.to_csv(‘dates_converted.csv’, index=False)
```

- 샘플 데이터는 [🔗여기](sampledata/5.10/README.md)를 참조해 주십시오.

## 5.11 CLI 틱택토 Python 프로그램을 Golang으로 변환하기

## 5.12 PyGame 오셀로 게임

```
PyGame을 사용하여 오셀로 게임을 만들어보겠습니다. 게임은 다음과 같은 기능들을 포함할 것입니다.
...
```

```
게임 종료 조건(판이 가득 차거나, 어느 한 쪽 플레이어의 돌이 사라진 경우)이나 승패 판정은 구현되어 있지 않지만, 기본적인 오셀로 게임의 기능은 갖추고 있습니다. 필요에 따라 추가 기능이나 수정 작업을 진행해 주세요.
```

## 5.13 웹 스크래핑 해보기

## 5.14 SQL 데이터베이스 다루고 집계하기

<kbd>CREATE_TABLE.sql</kbd>
```
-- 고객 테이블
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100)
);

-- 제품 테이블
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT
);

-- 주문 테이블
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 주문 상세 테이블
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```

<kbd>Query.sql</kbd>
```
SELECT
    c.FirstName || ‘ ‘ || c.LastName as CustomerName,
    o.OrderID,
    o.OrderDate,
    o.TotalAmount,
    GROUP_CONCAT(p.ProductName, ‘, ‘) as ProductNames
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
WHERE o.OrderDate >= ‘2023-01-01’
    AND o.OrderDate <= ‘2023-12-31’
    AND o.TotalAmount > 10000
GROUP BY o.OrderID
ORDER BY o.OrderDate;
```

## 📘 5.15 iOS 애플리케이션 개발(Swift)

샘플 코드는 아래 저장소에서 다운로드 해서 사용해 주십시오.

[「TipCalculator_ios」저장소](https://github.com/kinopeee/TipCalculator_ios)

```swift
import SwiftUI

struct ContentView: View {
    @State private var billAmount: String = “”
    @State private var tipPercentage: String = “”
    @State private var tipAmount: Double = 0.0
    @State private var totalAmount: Double = 0.0
    var body: some View {
        VStack {
            TextField(“청구 금액”, text: $billAmount)
                .keyboardType(.decimalPad)
                .padding()
                .border(Color.gray, width: 1)

            TextField(“팁 비율 (%)”, text: $tipPercentage)
                .keyboardType(.decimalPad)
                .padding()
                .border(Color.gray, width: 1)

            Button(action: calculateTip) {
                Text(“계산하기”)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }

            Text(“팁 금액: \(tipAmount, specifier: “%.2f”) 원”)
                .padding()

            Text(“총 금액: \(totalAmount, specifier: “%.2f”) 원”)
                .padding()
        }
        .padding()
    }

    func calculateTip() {
        guard let bill = Double(billAmount), let tipPercent = Double(tipPercentage) else {
            return
        }

        tipAmount = bill * (tipPercent / 100)
        totalAmount = bill + tipAmount
    }
}

#Preview {
    ContentView()
}
```

## 5.16 Android 애플리케이션 개발하기(Flutter)

샘플 코드는 아래 저장소에서 다운로드 해서 사용해 주십시오.

[「TipCalculator_flutter」 저장소](https://github.com/kinopeee/TipCalculator_flutter)

<kbd>spec1.md</kbd>
```
# 팁 계산기 (TipCal) 애플리케이션 사양서

## 1. 개요
이 애플리케이션은 식사 후 팁 계산을 도와주는 iOS 애플리케이션입니다. KRW와 USD 간의 환율 계산도 지원합니다.

## 2. 기술 스택
- 개발 언어: Swift
- 프레임워크: SwiftUI
- 최소 지원 OS: iOS (버전 정보 필요)

## 3. 주요 기능
### 3.1 기본 입력
- 청구 금액 입력 (KRW/USD)
- 통화 선택 기능 (KRW/USD 토글)
- 팁 비율 설정 (10% ~ 30%, 0.5% 단위 조절)

### 3.2 환율 기능
- USD 선택 시 환율 입력 가능
- 기본 환율: 1 USD = 1,300 KRW
- 사용자 정의 환율 설정 가능

### 3.3 계산 기능
- 팁 금액 자동 계산
- 총 금액 계산 (청구 금액 + 팁)
- USD 선택 시 KRW/USD 동시 표시

### 3.4 UI/UX 특징
- Form 기반의 직관적인 인터페이스
- 네비게이션 타이틀: “팁 계산기”
- 섹션별 구분된 정보 표시
- 청구 금액 입력
- 환율 설정 (USD 모드)
- 팁 비율 선택
- 팁 금액 표시
- 총 금액 표시

### 3.5 표시 형식
- KRW: 정수 표시 (소수점 없음)
- USD: 소수점 둘째 자리까지 표시
- 팁 비율: 소수점 첫째 자리까지 표시

## 4. 시각적 요소
- 팁 금액: 파란색으로 표시
- 총 금액: 녹색으로 표시 (굵은 글씨)
- 통화 기호
- KRW: ₩
- USD: $

## 5. 입력 제한
- 금액 입력: 숫자 키패드만 표시
- 환율 입력: 숫자 키패드만 표시
- 팁 비율: 슬라이더 사용 (10%~30% 범위)
```

```
구현할 수 없는 부분은 다음과 같습니다:
- NavigationView와 Form은 SwiftUI의 특정 구성 요소입니다. Flutter에서는 Scaffold와 Form 위젯을 사용하여 유사한 기능을 구현했습니다.
- @State는 SwiftUI의 상태 관리 기능입니다. Flutter에서는 StatefulWidget과 setState 메소드를 사용하여 상태 관리를 수행합니다.
```

<kbd>spec2.md</kbd>
```
# 팁 계산기 IOS 애플리케이션 사양서

## 기능
- 청구 금액을 입력하여 팁과 총액을 계산
- KRW(원화)와 USD(달러) 간 통화 변환 지원
- 팁 비율 조절 기능 (10%~30% 범위)
- 실시간 환율 설정 기능
- 통화별 금액 표시 (USD 입력 시 원화 금액 동시 표시)

## 동작
1. 청구 금액 입력
  - 숫자만 입력 가능 (소수점 허용)
  - 통화 선택에 따라 입력 필드 안내 텍스트 변경
  - 입력값이 없을 경우 0으로 처리

2. 통화 변환
  - USD/KRW 토글 스위치로 통화 선택
  - USD 선택 시 환율 입력 필드 표시
  - 기본 환율: 1 USD = 1,300 KRW
  - 사용자 정의 환율 설정 가능

3. 팁 계산
  - 입력된 금액에 선택된 팁 비율을 적용하여 계산
  - USD 입력 시 달러와 원화로 동시 표시
  - KRW 입력 시 원화로만 표시

## 함수
1. billAmountInKRW
  - 입력된 금액을 원화로 변환
  - USD 선택 시 환율을 적용하여 변환
  - 반환 타입: Double

2. tipAmount
  - 팁 금액 계산
  - 원화 기준 금액에 팁 비율 적용
  - 반환 타입: Double

3. totalAmount
  - 총 지불 금액 계산 (청구 금액 + 팁)
  - 반환 타입: Double

4. formattedTipPercentage
  - 팁 비율을 소수점 첫째 자리까지 표시
  - 반환 타입: String

## 화면 디자인
1. 네비게이션 바
  - 제목: “팁 계산기”

2. 입력 섹션
  - 청구 금액 입력 필드
  - USD/KRW 토글 스위치
  - 환율 설정 필드 (USD 모드에서만 표시)

3. 팁 비율 섹션
  - 슬라이더 컨트롤

4. 결과 표시 섹션
  - 팁 금액 섹션
    - USD 모드: 달러와 원화 동시 표시
    - KRW 모드: 원화만 표시
    - 파란색으로 강조
  - 총 금액 섹션
    - USD 모드: 달러와 원화 동시 표시
    - KRW 모드: 원화만 표시
    - 녹색으로 강조
    - 굵은 글씨 처리

## 조작성
1. 키보드
  - 청구 금액 입력: 숫자 키패드 (소수점 허용)
  - 환율 입력: 숫자 키패드 (소수점 허용)

2. 팁 비율 조절
  - 슬라이더로 직관적인 조작
  - 0.5% 단위로 미세 조정 가능
  - 범위: 10% ~ 30%

## 설정
1. 상태 관리 (@State)
  - billAmount: String (청구 금액)
  - tipPercentage: Double (팁 비율, 기본값 15.0%)
  - isUSD: Bool (통화 선택, 기본값 false)
  - exchangeRate: Double (환율, 기본값 1300.0)

2. 숫자 포맷
  - USD: 소수점 둘째 자리까지 표시
  - KRW: 정수로 표시 (소수점 없음)
  - 팁 비율: 소수점 첫째 자리까지 표시

3. 통화 기호
  - USD: $ 기호
  - KRW: ₩ 기호
```

<kbd>spec2_Flutter.md</kbd>
```
# 팁 계산기 애플리케이션 사양서 (Flutter 버전)

## 기능
- 청구 금액을 입력하여 팁과 총액을 계산
- KRW(원화)와 USD(달러) 간 통화 변환 지원
- 팁 비율 조절 기능 (10%~30% 범위)
- 실시간 환율 설정 기능
- 통화별 금액 표시 (USD 입력 시 원화 금액 동시 표시)

## 동작
1. 청구 금액 입력
  - 숫자만 입력 가능 (소수점 허용)
  - 통화 선택에 따라 입력 필드 안내 텍스트 변경
  - 입력값이 없을 경우 0으로 처리

2. 통화 변환
  - USD/KRW 토글 스위치로 통화 선택
  - USD 선택 시 환율 입력 필드 표시
  - 기본 환율: 1 USD = 1,300 KRW
  - 사용자 정의 환율 설정 가능

3. 팁 계산
  - 입력된 금액에 선택된 팁 비율을 적용하여 계산
  - USD 입력 시 달러와 원화로 동시 표시
  - KRW 입력 시 원화로만 표시

## 함수
1. calculateBillAmountInKRW
  - 입력된 금액을 원화로 변환
  - USD 선택 시 환율을 적용하여 변환
  - 반환 타입: double

2. calculateTipAmount
  - 팁 금액 계산
  - 원화 기준 금액에 팁 비율 적용
  - 반환 타입: double

3. calculateTotalAmount
  - 총 지불 금액 계산 (청구 금액 + 팁)
  - 반환 타입: double

4. formatTipPercentage
  - 팁 비율을 소수점 첫째 자리까지 표시
  - 반환 타입: String

## 화면 디자인
1. AppBar
  - 제목: “팁 계산기”

2. 입력 섹션
  - TextField: 청구 금액 입력 필드
  - Switch: USD/KRW 토글 스위치
  - TextField: 환율 설정 필드 (USD 모드에서만 표시)

3. 팁 비율 섹션
  - Slider 위젯

4. 결과 표시 섹션
  - 팁 금액 섹션
    - USD 모드: 달러와 원화 동시 표시
    - KRW 모드: 원화만 표시
    - TextStyle: color: Colors.blue
  - 총 금액 섹션
    - USD 모드: 달러와 원화 동시 표시
    - KRW 모드: 원화만 표시
    - TextStyle: color: Colors.green, fontWeight: FontWeight.bold

## 조작성
1. 키보드
  - 청구 금액 입력: TextInputType.numberWithOptions(decimal: true)
  - 환율 입력: TextInputType.numberWithOptions(decimal: true)

2. 팁 비율 조절
  - Slider 위젯 사용
  - divisions: 40 (0.5% 단위 조절을 위해)
  - min: 10.0, max: 30.0

## 설정
1. 상태 관리 (StatefulWidget)
  - billAmount: String (청구 금액)
  - tipPercentage: double (팁 비율, 기본값 15.0)
  - isUSD: bool (통화 선택, 기본값 false)
  - exchangeRate: double (환율, 기본값 1300.0)

2. 숫자 포맷
  - USD: NumberFormat(“#,##0.00”)
  - KRW: NumberFormat(“#,##0”)
  - 팁 비율: NumberFormat(“0.0”)
3. 통화 기호
  - USD: $ 기호
  - KRW: ₩ 기호

## 이식 시 주의사항
1. Form 위젯
  - iOS의 Form은 Flutter의 Column이나 ListView로 대체
  - iOS의 Section은 Flutter의 Card나 Container로 구현

2. 네비게이션
  - iOS의 NavigationView는 Flutter의 Scaffold와 AppBar 조합으로 구현

3. 상태 관리
  - SwiftUI의 @State는 Flutter의 setState() 메서드로 대체
  - 더 복잡한 상태 관리가 필요한 경우 Provider나 Riverpod 같은 상태 관리 라이브러리 사용 고려

4. 레이아웃
  - iOS의 Form 기반 레이아웃을 Flutter의 Material Design 또는 Cupertino 스타일로 재구성 필요
  - Padding, SizedBox 등을 활용하여 적절한 간격 조정 필요
```

<kbd>spec_flutter.v2.md</kbd>
```
**섹션: 팁 계산**

**DropdownButton 위젯**
- 선택지: 주요 통화 기호 (USD, EUR, JPY, AUD, CAD)

**청구 금액 입력**
- 라벨: “청구 금액”
- TextField: 플레이스홀더 “청구 금액을 입력”
- 키보드 타입: 소수점 입력 허용
- 팁 비율 슬라이더
  - 슬라이더 범위: 10% ~ 30%

**팁 비율 표시**
- 라벨: “팁 비율”
- 값: 슬라이더 값 (정수로 표시)

**설정된 팁 비율 표시**
- 라벨: “팁 비율”
- 값: 설정된 팁 비율 (소수 둘째 자리까지 표시)

**팁 금액 표시**
- 라벨: “팁 금액”
- 값: 계산된 팁 금액 (소수 둘째 자리까지 표시)
- 선택한 통화 단위에 따른 표시

**총액 표시**
- 라벨: “총 금액”
- 값: 계산된 총액 (소수 둘째 자리까지 표시)
- 선택한 통화 단위에 따른 표시

```