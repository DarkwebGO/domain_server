#!/bin/bash

# 현재 디렉토리의 모든 파일을 순회
for file in *; do
    # 파일 이름에서 'https:'를 포함하는지 확인
    if [[ "$file" == *"https:"* ]]; then
        # 'https:'를 '_'로 대체한 새 파일 이름 생성
        newname=$(echo "$file" | sed 's/https:/_/g')
        # 파일 이름 변경
        mv "$file" "$newname"
    fi
done

